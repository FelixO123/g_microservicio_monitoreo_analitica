from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- SCHEMAS PARA KPI ---
class KPIBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    valor: float

class KPICreate(KPIBase):
    pass

class KPIResponse(KPIBase):
    id_kpi: int
    fecha_calculo: datetime
    class Config:
        from_attributes = True


# --- SCHEMAS PARA METRICA PROYECTO ---
class MetricaBase(BaseModel):
    id_proyecto: int
    porcentaje_avance: float
    tareas_completadas: int
    tareas_totales: int

class MetricaCreate(MetricaBase):
    pass

class MetricaResponse(MetricaBase):
    id_metrica: int
    class Config:
        from_attributes = True

# --- SCHEMA PARA DASHBOARD ---
class DashboardData(BaseModel):
    kpis: List[KPIResponse]
    metricas: List[MetricaResponse]
    reportes_recientes: List[ReporteResponse]
