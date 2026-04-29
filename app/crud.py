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

# --- CRUD REPORTES ---
def get_reportes(db: Session):
    return db.query(models.Reporte).all()

def get_reporte(db: Session, reporte_id: int):
    return db.query(models.Reporte).filter(models.Reporte.id_reporte == reporte_id).first()

def create_reporte(db: Session, reporte: schemas.ReporteCreate):
    db_reporte = models.Reporte(**reporte.dict())
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)
    return db_reporte

def update_reporte(db: Session, reporte_id: int, reporte_data: schemas.ReporteCreate):
    db_reporte = db.query(models.Reporte).filter(models.Reporte.id_reporte == reporte_id).first()
    if db_reporte:
        for key, value in reporte_data.dict().items():
            setattr(db_reporte, key, value)
        db.commit()
        db.refresh(db_reporte)
    return db_reporte

def delete_reporte(db: Session, reporte_id: int):
    db_reporte = db.query(models.Reporte).filter(models.Reporte.id_reporte == reporte_id).first()
    if db_reporte:
        db.delete(db_reporte)
        db.commit()
    return db_reporte

# --- CRUD MÉTRICAS PROYECTOS ---
def get_metricas(db: Session):
    return db.query(models.MetricaProyecto).all()

def get_metrica(db: Session, metrica_id: int):
    return db.query(models.MetricaProyecto).filter(models.MetricaProyecto.id_metrica == metrica_id).first()
""""
def get_metrica_por_proyecto(db: Session, id_proyecto: int):
    return db.query(models.MetricaProyecto).filter(models.MetricaProyecto.id_proyecto == id_proyecto).first()
"""

def get_metrica_por_proyecto(db: Session, id_proyecto: int):
    return db.query(models.MetricaProyecto).filter(models.MetricaProyecto.id_proyecto == id_proyecto).all()
    
def create_metrica(db: Session, metrica: schemas.MetricaCreate):
    db_metrica = models.MetricaProyecto(**metrica.dict())
    db.add(db_metrica)
    db.commit()
    db.refresh(db_metrica)
    return db_metrica

def update_metrica(db: Session, metrica_id: int, metrica_data: schemas.MetricaCreate):
    db_metrica = get_metrica(db, metrica_id)
    if db_metrica:
        for key, value in metrica_data.dict().items():
            setattr(db_metrica, key, value)
        db.commit()
        db.refresh(db_metrica)
    return db_metrica

def delete_metrica(db: Session, metrica_id: int):
    db_metrica = get_metrica(db, metrica_id)
    if db_metrica:
        db.delete(db_metrica)
        db.commit()
    return db_metrica