from pydantic import BaseModel
from typing import Optional



class DonasiBase(BaseModel):
    nama_barang: str
    kategori: str
    kondisi: str
    deskripsi: str
    tanggal_donasi: str


class DonasiCreate(DonasiBase):
    donatur_id: int
    penerima_donasi_id: Optional[int] = None


class DonasiRead(DonasiBase):
    id: int

    class Config:
        orm_mode = True


class DonasiUpdate(DonasiBase):
    nama_barang: Optional[str] = None
    kategori: Optional[str] = None
    kondisi: Optional[str] = None
    deskripsi: Optional[str] = None
    tanggal_donasi: Optional[str] = None

    class Config:
        orm_mode = True


# --- Barang Rekomendasi Section ---
class BarangRekomendasiBase(BaseModel):
    barang_id: int
    penerima_id: int


class BarangRekomendasiCreate(BarangRekomendasiBase):
    layak: float


class BarangRekomendasiRead(BarangRekomendasiBase):
    id: int
    layak: float

    class Config:
        orm_mode = True


class BarangRekomendasiUpdate(BaseModel):
    layak: float

    class Config:
        orm_mode = True
