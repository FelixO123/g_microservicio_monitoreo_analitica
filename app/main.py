from fastapi import FastAPI

app = FastAPI()

#PROGRAMA DEFECTO PARA PRUEBA DEL SERVIDOR
"""
@app.get("/")
def read_root():
    return {"status": "OK", "message": "Servidor de FastAPI funcionando correctamente"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}
"""

#PROGRAMAR DE AQUI PARA ABAJO EL MICROSERVICIO

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud, services, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Microservicio de Monitoreo y Analítica")

# --- FUNCIONALIDAD CRUD PARA ENTIDAD KPI ---

@app.get("/api/analisis/kpi", response_model=List[schemas.KPIResponse])
def listar_kpis(db: Session = Depends(database.get_db)):
    return crud.get_kpis(db)

@app.get("/api/analisis/kpi/{id}", response_model=schemas.KPIResponse)
def obtener_kpi(id: int, db: Session = Depends(database.get_db)):
    db_kpi = crud.get_kpi(db, id)
    if not db_kpi:
        raise HTTPException(status_code=404, detail="KPI no encontrado")
    return db_kpi

@app.post("/api/analisis/kpi", response_model=schemas.KPIResponse)
def crear_kpi(kpi: schemas.KPICreate, db: Session = Depends(database.get_db)):
    return crud.create_kpi(db, kpi)

@app.put("/api/analisis/kpi/{id}", response_model=schemas.KPIResponse)
def actualizar_kpi(id: int, kpi: schemas.KPICreate, db: Session = Depends(database.get_db)):
    return crud.update_kpi(db, id, kpi)

@app.delete("/api/analisis/kpi/{id}")
def eliminar_kpi(id: int, db: Session = Depends(database.get_db)):
    crud.delete_kpi(db, id)
    return {"message": "KPI eliminado correctamente"}

# --- CRUD MÉTRICAS DE PROYECTOS ---

@app.get("/api/analisis/metricas", response_model=List[schemas.MetricaResponse])
def listar_todas_metricas(db: Session = Depends(database.get_db)):
    return crud.get_metricas(db)

@app.get("/api/analisis/metrica/{id_metrica}", response_model=schemas.MetricaResponse)
def obtener_metrica_especifica(id_metrica: int, db: Session = Depends(database.get_db)):
    return crud.get_metrica(db, id_metrica)
"""
@app.get("/api/analisis/metricas/proyectos/{id_proyecto}", response_model=schemas.MetricaResponse)
def metrica_por_proyecto(id_proyecto: int, db: Session = Depends(database.get_db)):
    return crud.get_metrica_por_proyecto(db, id_proyecto)
"""

@app.get("/api/analisis/metricas/proyectos/{id_proyecto}", response_model=List[schemas.MetricaResponse])
def metrica_por_proyecto(id_proyecto: int, db: Session = Depends(database.get_db)):
    metricas = crud.get_metrica_por_proyecto(db, id_proyecto)
    if not metricas:
        raise HTTPException(status_code=404, detail="No se encontraron métricas para este proyecto")
    return metricas

    
@app.post("/api/analisis/metrica", response_model=schemas.MetricaResponse)
def crear_metrica_proyecto(metrica: schemas.MetricaCreate, db: Session = Depends(database.get_db)):
    return crud.create_metrica(db, metrica)

@app.put("/api/analisis/metrica/{id_metrica}", response_model=schemas.MetricaResponse)
def actualizar_metrica_proyecto(id_metrica: int, metrica: schemas.MetricaCreate, db: Session = Depends(database.get_db)):
    return crud.update_metrica(db, id_metrica, metrica)

@app.delete("/api/analisis/metrica/{id_metrica}")
def eliminar_metrica(id_metrica: int, db: Session = Depends(database.get_db)):
    crud.delete_metrica(db, id_metrica)
    return {"message": "Métrica eliminada"}
