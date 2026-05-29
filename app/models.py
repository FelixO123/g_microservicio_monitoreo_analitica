from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime, timezone

class KPI(Base):
    __tablename__ = "kpis"
    id_kpi = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    valor = Column(Float)
    # Usamos timezone.utc para evitar problemas de horario
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
    
    # Esta es tu FK Lógica. No lleva ForeignKey("proyectos.id") 
    # porque la tabla proyectos NO existe en esta DB.
    # Añadimos unique=True para el control correcto en el CRUD.
    id_proyecto = Column(Integer, nullable=False, unique=True, index=True) 
    
    porcentaje_avance = Column(Float, default=0.0)  # CRÍTICO: Mantiene el soporte decimal
    tareas_completadas = Column(Integer, default=0)
    tareas_totales = Column(Integer, default=0)
    
    # Integrada la columna de fecha con el formato UTC consistente de tu proyecto
    fecha_calculo = Column(DateTime, default=lambda: datetime.now(timezone.utc))