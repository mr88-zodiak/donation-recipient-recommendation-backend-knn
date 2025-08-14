from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdminBase(BaseModel):
    username: str
    
    class Config:
        orm_mode = True

class AdminCreate(AdminBase):
    password: str

class AdminRead(BaseModel):
    username: str
    password: str
    
    class Config:
        orm_mode = True
class AdminUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    
    class Config:
        orm_mode = True
        
        
class DonaturBase(BaseModel):
    nama: str
    tempat_tinggal: Optional[str]
    no_telepon: Optional[str]
    alamat: Optional[str]
    
    class Config:
        orm_mode = True

class DonaturCreate(DonaturBase):
    email: str
    password: str

class DonaturRead(BaseModel):
    nama: str
    tempat_tinggal: str
    no_telepon: str
    alamat: str
    email: str
    password: str

    class Config:
        orm_mode = True
        
class DonaturUpdate(BaseModel):
    nama: Optional[str] = None
    tempat_tinggal: Optional[str] = None
    email: Optional[str] = None
    no_telepon: Optional[str] = None
    alamat: Optional[str] = None
    
    class Config:
        orm_mode = True


class penerimaDonasi(BaseModel):
    nama: str
    penghasilan_perbulan: int
    jumlah_tanggungan: int
    status_tempat_tinggal: str
    jumlah_kendaraan: int
    jenis_kebutuhan: str
    
    class Config:
        orm_mode = True

class penerimaDonasiCreate(penerimaDonasi):
    username: str
    password: str

class penerimaDonasiRead(BaseModel):
    id: int
    
    class Config:
        orm_mode = True
class penerimaDonasiUpdate(BaseModel):
    nama: Optional[str] = None
    penghasilan_perbulan: Optional[int] = None
    jumlah_tanggungan: Optional[int] = None
    status_tempat_tinggal: Optional[str] = None
    jumlah_kendaraan: Optional[int] = None
    jenis_kebutuhan: Optional[str] = None
    
class tesing(BaseModel):
    id: int
    username: str


class testingCreate(tesing):
    password: str

class testingRead(tesing):
    id: int
    
    class Config:
        orm_mode = True
        
class testingUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    
    class Config:
        orm_mode = True
        
        
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
        