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

