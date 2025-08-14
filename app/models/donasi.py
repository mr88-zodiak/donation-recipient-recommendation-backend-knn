from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship 
from datetime import datetime 
from app.db.database import Base 




class BarangDonasi(Base):
    __tablename__ = "barang_donasi"  # ← Ganti ini
    id = Column(Integer, primary_key=True, index=True)
    donatur_id = Column(Integer, ForeignKey("donatur.id"), nullable=False, index=True)
    penerima_donasi_id = Column(Integer, ForeignKey("penerima_donasi.id"), nullable=True, index=True)
    nama_barang = Column(String, nullable=False)
    kategori = Column(String, nullable=False)
    kondisi = Column(String, nullable=False)
    deskripsi = Column(Text, nullable=False)
    tanggal_donasi = Column(DateTime, default=datetime.utcnow, nullable=False)
    donatur_info = relationship("Donatur", back_populates="donasi")
    calon_penerima = relationship("BarangRekomendasi", back_populates="barang")

class BarangRekomendasi(Base):
    __tablename__ = "barang_rekomendasi"
    id = Column(Integer, primary_key=True)
    barang_id = Column(Integer, ForeignKey("barang_donasi.id"))
    penerima_id = Column(Integer, ForeignKey("penerima_donasi.id"))
    layak = Column(Float)
    barang = relationship("BarangDonasi", back_populates="calon_penerima")
    penerima = relationship("Penerima_Donasi", backref="barang_rekomendasi")
