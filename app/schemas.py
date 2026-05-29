from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# ==========================================
# --- SCHEMAS PARA KPI ---------------------
# ==========================================
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


# ==========================================
# --- SCHEMAS PARA REPORTE -----------------
# ==========================================
class ReporteBase(BaseModel):
    resumen: str
    estado_general: str

class ReporteCreate(ReporteBase):
    pass

class ReporteResponse(ReporteBase):
    id_reporte: int
    fecha_generacion: datetime
    
    class Config:
        from_attributes = True


# ==========================================
# --- SCHEMAS PARA METRICA PROYECTO --------
# ==========================================
class MetricaBase(BaseModel):
    id_proyecto: int
    porcentaje_avance: float
    tareas_completadas: int
    tareas_totales: int

# Integrado explícitamente según tus requerimientos para asegurar el tipado float
class MetricaCreate(BaseModel):
    id_proyecto: int
    porcentaje_avance: float  
    tareas_completadas: int
    tareas_totales: int

class MetricaResponse(MetricaBase):
    id_metrica: int
    # Mantenemos fecha_calculo opcional para evitar cualquier tipo de error en el mapeo con el Frontend
    fecha_calculo: Optional[datetime] = None 
    
    class Config:
        from_attributes = True


# ==========================================
# --- SCHEMA PARA DASHBOARD ----------------
# ==========================================
# Este objeto consolida la respuesta exacta que consume tu DashboardAnalitica.jsx
class DashboardData(BaseModel):
    kpis: List[KPIResponse]
    metricas: List[MetricaResponse]
    reportes_recientes: List[ReporteResponse]