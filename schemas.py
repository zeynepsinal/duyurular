from pydantic import BaseModel
from datetime import datetime

class DuyuruCreate(BaseModel):
    baslik: str
    icerik: str
    saat: str
    yazar: str
    kategori: str
    is_important: bool

class DuyuruResponse(DuyuruCreate):
    id: int
    tarih: datetime

    class Config:
        orm_mode = True
