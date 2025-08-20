from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
import pandas as pd
import joblib
import uuid
import os
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.rekomendasi import read_all_rekomendasi
from app.schemas.hasilRekomendasi import HasilRekomendasiBase
from app.schemas.response import SuksesResponGet
from app.models.HasilRekomedasi import HasilRekomendasi

sr = APIRouter()

@sr.post("/rekomendasi/upload", tags=["recomendation system"])
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    output_filename = None
    try:
        # Baca file
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        else:
            raise HTTPException(status_code=400, detail="File harus CSV atau Excel")
        
        # Debug: Print kolom asli
        print(f"Kolom asli: {list(df.columns)}")
        
        # Normalisasi nama kolom - buat lowercase dan strip spasi
        df.columns = [c.strip().lower() for c in df.columns]
        print(f"Kolom setelah normalisasi: {list(df.columns)}")
        
        # Mapping kolom yang lebih komprehensif
        col_map = {
            # Format dengan spasi
            "penghasilan perbulan": "penghasilanPerbulan",
            "penghasilan per bulan": "penghasilanPerbulan", 
            "penghasilan_perbulan": "penghasilanPerbulan",
            "penghasilan_per_bulan": "penghasilanPerbulan",
            "penghasilan": "penghasilanPerbulan",
            "income": "penghasilanPerbulan",
            
            # Format camelCase tanpa spasi (sesuai dengan file Anda)
            "penghasilanperbulan": "penghasilanPerbulan",
            "jumlahtanggungan": "jumlahTanggungan", 
            "statustempattinggal": "statusTempatTinggal",
            "jumlahkendaraan": "jumlahKendaraan",
            "jeniskebutuhan": "jenisKebutuhan",
            
            # Format dengan spasi dan underscore lainnya
            "jumlah tanggungan": "jumlahTanggungan",
            "jumlah_tanggungan": "jumlahTanggungan",
            "tanggungan": "jumlahTanggungan",
            "dependents": "jumlahTanggungan",
            
            "status tempat tinggal": "statusTempatTinggal",
            "status_tempat_tinggal": "statusTempatTinggal",
            "tempat tinggal": "statusTempatTinggal",
            "tempat_tinggal": "statusTempatTinggal",
            "housing": "statusTempatTinggal",
            
            "jumlah kendaraan": "jumlahKendaraan",
            "jumlah_kendaraan": "jumlahKendaraan",
            "kendaraan": "jumlahKendaraan",
            "vehicle": "jumlahKendaraan",
            
            "jenis kebutuhan": "jenisKebutuhan",
            "jenis_kebutuhan": "jenisKebutuhan",
            "kebutuhan": "jenisKebutuhan",
            "need": "jenisKebutuhan",
            
            "nama": "nama",
            "name": "nama"
        }
        
        # Lakukan mapping
        df = df.rename(columns=col_map)
        print(f"Kolom setelah mapping: {list(df.columns)}")
        
        # Daftar kolom yang diperlukan
        required_cols = [
            "nama", "penghasilanPerbulan", "jumlahTanggungan",
            "statusTempatTinggal", "jumlahKendaraan", "jenisKebutuhan"
        ]
        
        # Validasi kolom yang diperlukan
        missing_cols = []
        for col in required_cols:
            if col not in df.columns:
                missing_cols.append(col)
        
        if missing_cols:
            available_cols = list(df.columns)
            error_msg = f"Kolom yang hilang: {missing_cols}. Kolom yang tersedia: {available_cols}"
            print(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Validasi data tidak kosong
        if df.empty:
            raise HTTPException(status_code=400, detail="File kosong atau tidak memiliki data")
        
        # Bersihkan data dan konversi tipe data
        try:
            # Konversi ke tipe data yang sesuai
            df["penghasilanPerbulan"] = pd.to_numeric(df["penghasilanPerbulan"], errors='coerce')
            df["jumlahTanggungan"] = pd.to_numeric(df["jumlahTanggungan"], errors='coerce')
            df["jumlahKendaraan"] = pd.to_numeric(df["jumlahKendaraan"], errors='coerce')
            
            # Hapus baris dengan data yang tidak valid
            df = df.dropna(subset=["penghasilanPerbulan", "jumlahTanggungan", "jumlahKendaraan"])
            
            if df.empty:
                raise HTTPException(status_code=400, detail="Tidak ada data valid setelah pembersihan")
                
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error dalam konversi data: {str(e)}")
        
        # Load model dan lakukan prediksi
        try:
            pipeline = joblib.load("./app/router/knn_model.pkl")
            
            # Buat DataFrame dengan nama kolom yang diharapkan model (dengan spasi)
            model_df = pd.DataFrame()
            model_df["penghasilan perbulan"] = df["penghasilanPerbulan"]
            model_df["jumlah tanggungan"] = df["jumlahTanggungan"] 
            model_df["status tempat tinggal"] = df["statusTempatTinggal"]
            model_df["jumlah kendaraan"] = df["jumlahKendaraan"]
            model_df["jenis kebutuhan"] = df["jenisKebutuhan"]
            
            # Lakukan prediksi dengan DataFrame yang sudah disesuaikan
            predictions = pipeline.predict(model_df)
            df["layak"] = predictions
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error dalam prediksi model: {str(e)}")
        
        # Simpan ke database
        try:
            objs = []
            for _, row in df.iterrows():
                obj = HasilRekomendasi(
                    nama=str(row["nama"]),
                    penghasilanPerbulan=int(row["penghasilanPerbulan"]),
                    jumlahTanggungan=int(row["jumlahTanggungan"]),
                    statusTempatTinggal=str(row["statusTempatTinggal"]),
                    jumlahKendaraan=int(row["jumlahKendaraan"]),
                    jenisKebutuhan=str(row["jenisKebutuhan"]),
                    layak=int(row["layak"]),
                )
                objs.append(obj)
            
            db.bulk_save_objects(objs)
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error menyimpan ke database: {str(e)}")
        
        # Simpan file Excel hasil
        output_filename = f"hasil_rekomendasi_{uuid.uuid4().hex}.xlsx"
        df.to_excel(output_filename, index=False)
        
        def cleanup_file(file_path: str):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass
        
        # Buat background task untuk cleanup setelah file dikirim
        background_tasks = BackgroundTasks()
        background_tasks.add_task(cleanup_file, output_filename)
        
        return FileResponse(
            output_filename,
            filename="hasil_rekomendasi.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            background=background_tasks
        )
        
    except HTTPException:
        # Re-raise HTTPException tanpa wrapping
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        # Cleanup file jika ada error
        if 'output_filename' in locals() and output_filename and os.path.exists(output_filename):
            try:
                os.remove(output_filename)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@sr.get("/rekomendasi/getData", response_model=SuksesResponGet[HasilRekomendasiBase], tags=["recomendation system"])
def getData(db: Session = Depends(get_db)):
    try:
        getData = read_all_rekomendasi(db)
        return SuksesResponGet(status_code=200, data=getData)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error mengambil data: {str(e)}")