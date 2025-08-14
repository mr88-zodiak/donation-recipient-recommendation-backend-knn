from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from itsdangerous import URLSafeSerializer
from app.schemas.user import *
from app.schemas.donasi import *
from app.schemas.response import *
from datetime import timedelta
from app.crud.donasi import *
from app.crud.user import *
from app.db.session import get_db
from app.models.user import *
from app.models.donasi import *
from app.db.database import Base
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils.auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
import base64
from urllib.parse import quote

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



@router.get("/admin/getData", tags=["users"],response_model=SuksesResponGet[AdminRead])
def adminGetData(db: Session = Depends(get_db)):
    getData = read_admin(db)
    return SuksesResponGet(status_code=200, data=getData)

@router.get("/admin/getData/{id}", tags=["users"],response_model=SuksesResponGet[AdminRead])
def adminGetData(id: int, db: Session = Depends(get_db)):
    getDataId = read_adminID(db, id)
    return SuksesResponId(status_code=200, data=[getDataId])

@router.get("/donatur/getData", tags=["users"],response_model=SuksesResponGet[DonaturRead])
def donaturGetData(db: Session = Depends(get_db)):
    getData = read_donatur(db)
    return SuksesResponGet(status_code=200, data=getData)
    
@router.get("/penerima/getData", tags=["users"],response_model=SuksesResponGet[penerimaDonasiRead])
def penerimaGetData(db: Session = Depends(get_db)):
    getData = read_penerima(db)
    return SuksesResponGet(status_code=200, data=getData)




@router.post("/admin/AddData", tags=["users"],response_model=SuksesRespon)
def adminAdd(admin: AdminCreate, db: Session = Depends(get_db)):
    try:
        create_admin(db, admin)
        return SuksesRespon(status_code=200, message="Data berhasil ditambahkan")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/donatur/login", tags=["users"], response_model=Token)
def donaturLogin(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password
    loginDonatur = login_donatur(db, email, password)
    if not loginDonatur or not verify_password(form_data.password, loginDonatur.password):
        raise HTTPException(status_code=400, detail="username dan password salah!")

    access_token = create_access_token(
        {"sub": loginDonatur.nama},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/admin/login", tags=["users"], response_model=Token)
def adminLogin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = login_admin(db, form_data.username, form_data.password)
    print(admin.password)
    if not admin or not verify_password(form_data.password, admin.password):
        raise HTTPException(status_code=400, detail="username dan password salah!")

    access_token = create_access_token(
        {"sub": admin.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/donatur/AddData", tags=["users"],response_model=SuksesRespon)
def donaturAdd(db: Session = Depends(get_db), donatur: DonaturCreate = Depends()):
    try:
        create_donatur(db, donatur)
        return SuksesRespon(status_code=200, message="Data berhasil ditambahkan")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
@router.post("/penerima/AddData", tags=["users"],response_model=SuksesRespon)
def penerimaAdd(db: Session = Depends(get_db), penerima: penerimaDonasiCreate = Depends()):
    try:
        create_penerima(db, penerima)
        return SuksesRespon(status_code=200, message="Data berhasil ditambahkan")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
@router.post("/penerima/login", tags=["users"])
def penerimaLogin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password
    loginPenerima = login_penerima(db, email, password)
    if not loginPenerima or not verify_password(form_data.password, loginPenerima.password):
        raise HTTPException(status_code=400, detail="username dan password salah!")

    access_token = create_access_token(
        {"sub": loginPenerima.nama},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}





@router.put("/donatur/updateData/{id}", tags=["users"],response_model=SuksesRespon)
def donaturupdate(id: int, db: Session = Depends(get_db), donatur: DonaturUpdate = Depends()):
    try:
        update_donatur(db, id, donatur)
        return SuksesRespon(status_code=200, message="Data berhasil diupdate")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
@router.put("/penerima/updateData/{id}", tags=["users"],response_model=SuksesRespon)
def penerimaUpdate(id: int, db: Session = Depends(get_db), penerima: penerimaDonasiUpdate = Depends()):
    try:
        update_penerima(db, id, penerima)
        return SuksesRespon(status_code=200, message="Data berhasil diupdate")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
        



@router.delete("/donatur/deleteData/{id}", tags=["users"],response_model=SuksesRespon)
def donaturDelete(id: int, db: Session = Depends(get_db)):
    try:
        delete_donatur(db, id)
        return SuksesRespon(status_code=200, message="Data berhasil dihapus")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("/penerima/deleteData/{id}", tags=["users"],response_model=SuksesRespon)
def penerimaDelete(id: int, db: Session = Depends(get_db)):
    try:
        delete_penerima(db, id)
        return SuksesRespon(status_code=200, message="Data berhasil dihapus")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("/admin/deleteData/{id}", tags=["users"],response_model=SuksesRespon)
def adminDelete(id: int, db: Session = Depends(get_db)):
    try:
        delete_admin(db, id)
        return SuksesRespon(status_code=200, message="Data berhasil dihapus")
    except(Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

