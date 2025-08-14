from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship 
from datetime import datetime 
from app.db.database import Base 


class Penerima_Donasi(Base):
    __tablename__ = "penerima_donasi"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    penghasilan_perbulan = Column(Integer)
    jumlah_tanggungan = Column(Integer)
    status_tempat_tinggal = Column(String)
    jumlah_kendaraan = Column(Integer)
    jenis_kebutuhan = Column(String)
    donasi_diterima = relationship("BarangDonasi", backref="penerima_donasi_target")

class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    time_stamp = Column(DateTime, default=datetime.now, nullable=False)

class Donatur(Base):
    __tablename__ = "donatur"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, index=True, nullable=False)
    tempat_tinggal = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    no_telepon = Column(String, unique=True, index=True)
    alamat = Column(Text)
    donasi = relationship("BarangDonasi", back_populates="donatur_info")

