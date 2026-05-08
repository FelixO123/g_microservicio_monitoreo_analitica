from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime, timezone

class KPI(Base):
    __tablename__ = "kpis"
    id_kpi = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    valor = Column(Float)
    fecha_calculo = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Reporte(Base):
    __tablename__ = "reportes"
    id_reporte = Column(Integer, primary_key=True, index=True)
    fecha_generacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resumen = Column(String)
    estado_general = Column(String)

class MetricaProyecto(Base):
    __tablename__ = "metricas_proyecto"
    id_metrica = Column(Integer, primary_key=True, index=True)
    # FK Lógica al microservicio de Proyectos
    id_proyecto = Column(Integer, nullable=False, index=True) 
    porcentaje_avance = Column(Float, default=0.0)
    tareas_completadas = Column(Integer, default=0)
    tareas_totales = Column(Integer, default=0)
    # NUEVO: Para saber cuándo se sincronizó por última vez
    fecha_actualizacion = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))