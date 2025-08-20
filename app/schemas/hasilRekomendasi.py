from pydantic import BaseModel

class HasilRekomendasiBase(BaseModel):
    id: int
    nama: str
    penghasilanPerbulan: int
    jumlahTanggungan: int
    statusTempatTinggal: str
    jumlahKendaraan: int
    jenisKebutuhan: str
    layak: int

    class Config:
        orm_mode = True
