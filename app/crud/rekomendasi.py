from sqlalchemy.orm import Session
from app.models.HasilRekomedasi import HasilRekomendasi

def read_all_rekomendasi(db: Session):
    return db.query(HasilRekomendasi).all()
