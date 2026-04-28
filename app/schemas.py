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

