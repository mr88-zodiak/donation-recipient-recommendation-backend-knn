from sqlalchemy.orm import Session
from app.schemas.user import *
from app.models.user import Admin, Donatur, Penerima_Donasi
from app.utils.Security import *
from datetime import datetime


def create_admin(db: Session, admin: AdminCreate):
    # Cek dulu username
    cek = db.query(Admin).filter(Admin.username == admin.username).first()
    if cek:
        raise ValueError("Username telah digunakan")

    hashed_password = hash_password(admin.password)
    db_admin = Admin(
        username=admin.username,
        password=hashed_password
    )

    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def create_donatur(db: Session, donatur: DonaturCreate):
    cek = db.query(Donatur).filter(Donatur.email == donatur.email).first()
    if cek:
        raise ValueError("Email telah digunakan")
    hashed_password = hash_password(donatur.password)
    db_donatur = Donatur(
        nama=donatur.nama, 
        tempat_tinggal=donatur.tempat_tinggal, 
        no_telepon=donatur.no_telepon, 
        alamat=donatur.alamat,
        email=donatur.email, 
        password=hashed_password)
    db.add(db_donatur)
    
    db.commit()
    db.refresh(db_donatur)
    return db_donatur

def create_penerima(db: Session, penerima: penerimaDonasiCreate):
    cek = db.query(Penerima_Donasi).filter(Penerima_Donasi.email == penerima.email).first()
    if cek:
        raise ValueError("Email telah digunakan")
    hashed_password = hash_password(penerima.password)
    db_penerima = Penerima_Donasi(
        nama=penerima.nama, 
        email=penerima.email, 
        password=hashed_password, 
        penghasilan_perbulan=penerima.penghasilan_perbulan, 
        jumlah_tanggungan=penerima.jumlah_tanggungan, 
        status_tempat_tinggal=penerima.status_tempat_tinggal, 
        jumlah_kendaraan=penerima.jumlah_kendaraan, 
        jenis_kebutuhan=penerima.jenis_kebutuhan)

    db.add(db_penerima)
    db.commit()
    db.refresh(db_penerima)
    return db_penerima



def read_admin(db: Session):
    return db.query(Admin).all()

def read_donatur(db: Session):
    return db.query(Donatur).all()

def read_penerima(db: Session):
    return db.query(Penerima_Donasi).all()

def read_adminID(db: Session, admin_id: int):
    return db.query(Admin).filter(Admin.id == admin_id).first()

def read_donaturID(db: Session, donatur_id: int):
    return db.query(Donatur).filter(Donatur.id == donatur_id).first()

def read_penerimaID(db: Session, penerima_id: int):
    return db.query(Penerima_Donasi).filter(Penerima_Donasi.id == penerima_id).first()


def update_admin(db: Session, admin_id: int, admin: AdminUpdate):
    db.query(Admin).filter(Admin.id == admin_id).update(admin.dict())
    db.commit()
    return db.query(Admin).filter(Admin.id == admin_id).first()

def update_donatur(db: Session, donatur_id: int, donatur: DonaturUpdate):
    db.query(Donatur).filter(Donatur.id == donatur_id).update(donatur.dict())
    db.commit()
    return db.query(Donatur).filter(Donatur.id == donatur_id).first()

def update_penerima(db: Session, penerima_id: int, penerima: penerimaDonasiUpdate):
    db.query(Penerima_Donasi).filter(Penerima_Donasi.id == penerima_id).update(penerima.dict())
    db.commit()
    return db.query(Penerima_Donasi).filter(Penerima_Donasi.id == penerima_id).first()

def delete_admin(db: Session, admin_id: int):
    db.query(Admin).filter(Admin.id == admin_id).delete()
    db.commit()

def delete_donatur(db: Session, donatur_id: int):
    db.query(Donatur).filter(Donatur.id == donatur_id).delete()
    db.commit()

def delete_penerima(db: Session, penerima_id: int):
    db.query(Penerima_Donasi).filter(Penerima_Donasi.id == penerima_id).delete()
    db.commit()
    
# login admin

def login_admin(db: Session, username: str, password: str):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        return False
    if not verify_password(password, admin.password):
        return False
    return admin

# login donatur

def login_donatur(db: Session, email: str, password: str):
    donatur = db.query(Donatur).filter(Donatur.email == email).first()
    if not donatur:
        return False
    if not verify_password(password, donatur.password):
        return False
    return donatur

def login_penerima(db: Session, email: str, password: str):
    penerima = db.query(Penerima_Donasi).filter(Penerima_Donasi.email == email).first()
    if not penerima:
        return False
    if not verify_password(password, penerima.password):
        return False
    return penerima



def daftar_donatur(db: Session, donatur: DonaturCreate):
    hashed_password = hash_password(donatur.password)
    db_donatur = Donatur(donatur.nama, donatur.tempat_tinggal, donatur.no_telepon, donatur.alamat,donatur.email, hashed_password)
    db.add(db_donatur)
    db.commit()
    db.refresh(db_donatur)
    return db_donatur

def daftar_penerima(db: Session, penerima: penerimaDonasiCreate):
    hashed_password = hash_password(penerima.password)
    db_penerima = Penerima_Donasi(penerima.nama, penerima.penghasilan_perbulan,penerima.jumlah_tanggungan,penerima.status_tempat_tinggal,penerima.jumlah_kendaraan,penerima.jenis_kebutuhan,penerima.username, hashed_password)
    db.add(db_penerima)
    db.commit()
    db.refresh(db_penerima)
    return db_penerima