from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.schemas.user import *
from app.crud.donasi import *
from app.db.session import get_db
from app.schemas.response import *
# from urllib.parse import quote
import base64

donasi_router = APIRouter()

@donasi_router.post("/donasikita/barang/AddData", tags=["donasi"],response_model=SuksesRespon)
def addData(donasi: DonasiCreate, db: Session = Depends(get_db)):
    try:
        create_donasi(db, donasi)
        return SuksesRespon(status_code=200, message="Data berhasil ditambahkan")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    

@donasi_router.get("/donasikita/barang/getData", tags=["donasi"])
def getData(db: Session = Depends(get_db)):
    getData = read_all_donasi(db)
    return SuksesResponGet(status_code=200, data=getData)

@donasi_router.delete("/donasikita/barang/deleteData/{id}", tags=["donasi"],response_model=SuksesRespon)
def barang(id: int, db: Session = Depends(get_db)):
    try:
        delete_donasi(db, id)
        return SuksesRespon(status_code=200, message="Data berhasil dihapus")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@donasi_router.put("/donasikita/barang/updateData/{id}", tags=["donasi"],response_model=SuksesRespon)
def barang(id: int,db: Session = Depends(get_db), donasi: DonasiUpdate = Depends()):
    try:
        update_donasi(db, id, donasi)
        return SuksesRespon(status_code=200, message="Data berhasil diupdate")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )