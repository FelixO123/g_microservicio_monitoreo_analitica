from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime, timezone

class MetricaProyecto(Base):
    __tablename__ = "metricas_proyecto"
    id_metrica = Column(Integer, primary_key=True, index=True)
    # Esta es tu FK Lógica. No lleva ForeignKey("proyectos.id") 
    # porque la tabla proyectos NO existe en esta DB.
    id_proyecto = Column(Integer, nullable=False, index=True) 
    porcentaje_avance = Column(Float, default=0.0)
    tareas_completadas = Column(Integer, default=0)
    tareas_totales = Column(Integer, default=0)