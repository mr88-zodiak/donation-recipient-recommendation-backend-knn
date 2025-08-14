from sqlalchemy.orm import Session
from app.schemas.donasi import *
from app.models.donasi import BarangDonasi,BarangRekomendasi


def create_donasi(db: Session, donasi: DonasiCreate):
    db_donasi = BarangDonasi(**donasi.dict())
    db.add(db_donasi)
    db.commit()
    db.refresh(db_donasi)
    return db_donasi

def read_donasi(db: Session, donasi_id: int):
    return db.query(BarangDonasi).filter(BarangDonasi.id == donasi_id).first()

def read_all_donasi(db: Session):
    return db.query(BarangDonasi).all()
def update_donasi(db: Session, donasi_id: int, donasi: BarangRekomendasiUpdate):
    db.query(BarangDonasi).filter(BarangDonasi.id == donasi_id).update(donasi.dict())
    db.commit()
    return db.query(BarangDonasi).filter(BarangDonasi.id == donasi_id).first()

def delete_donasi(db: Session, donasi_id: int):
    db.query(BarangDonasi).filter(BarangDonasi.id == donasi_id).delete()
    db.commit()
    
def create_rekomendasi(db: Session, rekomendasi: BarangRekomendasiCreate):
    db_rekomendasi = BarangRekomendasi(**rekomendasi.dict())
    db.add(db_rekomendasi)
    db.commit()
    db.refresh(db_rekomendasi)
    return db_rekomendasi

    