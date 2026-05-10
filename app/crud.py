from sqlalchemy.orm import Session
from . import models, schemas

# --- CRUD KPI ---
def get_kpis(db: Session):
    return db.query(models.KPI).all()

def get_kpi(db: Session, kpi_id: int):
    return db.query(models.KPI).filter(models.KPI.id_kpi == kpi_id).first()

def create_kpi(db: Session, kpi: schemas.KPICreate):
    db_kpi = models.KPI(**kpi.model_dump())
    db.add(db_kpi)
    db.commit()
    db.refresh(db_kpi)
    return db_kpi

def update_kpi(db: Session, kpi_id: int, kpi_data: schemas.KPICreate):
    db_kpi = get_kpi(db, kpi_id)
    if db_kpi:
        for key, value in kpi_data.model_dump().items():
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
    # INTEGRACIÓN: Ordenamos por fecha descendente para que el front muestre lo más nuevo
    return db.query(models.Reporte).order_by(models.Reporte.fecha_generacion.desc()).all()

def get_reporte(db: Session, reporte_id: int):
    return db.query(models.Reporte).filter(models.Reporte.id_reporte == reporte_id).first()

def create_reporte(db: Session, reporte: schemas.ReporteCreate):
    db_reporte = models.Reporte(**reporte.model_dump())
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)
    return db_reporte

def update_reporte(db: Session, reporte_id: int, reporte_data: schemas.ReporteCreate):
    db_reporte = db.query(models.Reporte).filter(models.Reporte.id_reporte == reporte_id).first()
    if db_reporte:
        for key, value in reporte_data.model_dump().items():
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
    # Ordenamos por las más recientes también
    return db.query(models.MetricaProyecto).all()

def get_metrica(db: Session, metrica_id: int):
    return db.query(models.MetricaProyecto).filter(models.MetricaProyecto.id_metrica == metrica_id).first()

def get_metrica_por_proyecto(db: Session, id_proyecto: int):
    # Nota: .first() suele ser mejor si solo esperamos una métrica por proyecto
    return db.query(models.MetricaProyecto).filter(models.MetricaProyecto.id_proyecto == id_proyecto).all()

def create_metrica(db: Session, metrica: schemas.MetricaCreate):
    db_metrica = models.MetricaProyecto(**metrica.model_dump())
    db.add(db_metrica)
    db.commit()
    db.refresh(db_metrica)
    return db_metrica

# --- LÓGICA DE SINCRONIZACIÓN (UPSERT) ---
def update_or_create_metrica(db: Session, metrica: schemas.MetricaCreate):
    # 1. Buscamos si ya existe una métrica para ese ID de proyecto específico
    db_metrica = db.query(models.MetricaProyecto).filter(
        models.MetricaProyecto.id_proyecto == metrica.id_proyecto
    ).first()

    if db_metrica:
        # 2. Si existe, actualizamos sus valores actuales
        db_metrica.porcentaje_avance = metrica.porcentaje_avance
        db_metrica.tareas_completadas = metrica.tareas_completadas
        db_metrica.tareas_totales = metrica.tareas_totales
        db.commit()
        db.refresh(db_metrica)
        return db_metrica
    
    # 3. Si no existe, usamos la función de creación estándar
    return create_metrica(db, metrica)

def update_metrica(db: Session, metrica_id: int, metrica_data: schemas.MetricaCreate):
    db_metrica = get_metrica(db, metrica_id)
    if db_metrica:
        for key, value in metrica_data.model_dump().items():
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