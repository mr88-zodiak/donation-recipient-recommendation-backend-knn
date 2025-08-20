from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship 
from datetime import datetime 
from app.db.database import Base 


class HasilRekomendasi(Base):
    __tablename__ = "hasilRekomendasi"
    id = Column(Integer, primary_key=True)
    nama = Column(String, nullable=False)
    penghasilanPerbulan = Column(Integer, nullable=False)
    jumlahTanggungan = Column(Integer, nullable=False)
    statusTempatTinggal = Column(String, nullable=False)
    jumlahKendaraan = Column(Integer, nullable=False)
    jenisKebutuhan = Column(String, nullable=False)
    layak = Column(Integer, nullable=False)