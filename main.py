from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from database import SessionLocal, engine
import models
import schemas 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/duyurular", response_model=list[schemas.DuyuruResponse])
def duyurulari_getir(db: Session = Depends(get_db)):
    return db.query(models.Duyuru).all()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/duyurular", response_model=schemas.DuyuruResponse)
def duyuru_ekle(duyuru: schemas.DuyuruCreate, db: Session = Depends(get_db)):
    yeni = models.Duyuru(**duyuru.dict())
    db.add(yeni)
    db.commit()
    db.refresh(yeni)
    return yeni

@app.get("/duyurular", response_model=list[schemas.DuyuruResponse])
def duyurulari_getir(
    is_important: Optional[bool] = None,
    kategori: Optional[str] = None,
    tarih: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Duyuru)

    if is_important is not None:
        query = query.filter(models.Duyuru.is_important == is_important)

    if kategori:
        query = query.filter(models.Duyuru.kategori.ilike(f"%{kategori}%"))

    if tarih:
        try:
            tarih_dt = datetime.strptime(tarih, "%Y-%m-%d").date()
            query = query.filter(models.Duyuru.tarih.cast(DateTime).contains(tarih_dt))
        except:
            raise HTTPException(status_code=400, detail="Tarih formatı yanlış.")

    return query.all()

@app.get("/duyurular/{id}", response_model=schemas.DuyuruResponse)
def duyuru_getir(id: int, db: Session = Depends(get_db)):
    duyuru = db.query(models.Duyuru).filter(models.Duyuru.id == id).first()
    if not duyuru:
        raise HTTPException(status_code=404, detail="Duyuru bulunamadı")
    return duyuru

@app.put("/duyurular/{id}", response_model=schemas.DuyuruResponse)
def duyuru_guncelle(id: int, yeni_duyuru: schemas.DuyuruCreate, db: Session = Depends(get_db)):
    duyuru = db.query(models.Duyuru).filter(models.Duyuru.id == id).first()
    if not duyuru:
        raise HTTPException(status_code=404, detail="Duyuru bulunamadı")

    for field, value in yeni_duyuru.dict().items():
        setattr(duyuru, field, value)

    db.commit()
    db.refresh(duyuru)
    return duyuru

@app.delete("/duyurular/{id}")
def duyuru_sil(id: int, db: Session = Depends(get_db)):
    duyuru = db.query(models.Duyuru).filter(models.Duyuru.id == id).first()
    if not duyuru:
        raise HTTPException(status_code=404, detail="Duyuru bulunamadı")

    db.delete(duyuru)
    db.commit()
    return {"message": f"{id} numaralı duyuru silindi"}
