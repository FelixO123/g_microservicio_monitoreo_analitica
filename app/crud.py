#PRUEBA DE QUE NO COMETI ERROR
from sqlalchemy.orm import Session
from . import models, schemas

# --- CRUD KPI ---
def get_kpis(db: Session):
    return db.query(models.KPI).all()

def get_kpi(db: Session, kpi_id: int):
    return db.query(models.KPI).filter(models.KPI.id_kpi == kpi_id).first()

def create_kpi(db: Session, kpi: schemas.KPICreate):
    db_kpi = models.KPI(**kpi.dict())
    db.add(db_kpi)
    db.commit()
    db.refresh(db_kpi)
    return db_kpi

def update_kpi(db: Session, kpi_id: int, kpi_data: schemas.KPICreate):
    db_kpi = get_kpi(db, kpi_id)
    if db_kpi:
        for key, value in kpi_data.dict().items():
            setattr(db_kpi, key, value)
        db.commit()
        db.refresh(db_kpi)
    return db_kpi

def delete_kpi(db: Session, kpi_id: int):
    db_kpi = get_kpi(db, kpi_id)
    if db_kpi:
        db.delete(db_kpi)
        db.commit()
    return db_kpi

