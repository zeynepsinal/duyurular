from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from database import Base

from datetime import datetime


class Duyuru(Base):
    __tablename__ = "duyurular"

    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String, nullable=False)
    icerik = Column(Text, nullable=False)
    tarih = Column(DateTime, default=datetime.utcnow)
    saat = Column(String, default="18:00")
    yazar = Column(String, default="Admin")
    kategori = Column(String, default="Genel")
    is_important = Column(Boolean, default=False)
