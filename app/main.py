from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud, database

# 1. Crear las tablas en la base de datos al arrancar
models.Base.metadata.create_all(bind=database.engine)

# 2. Instanciar FastAPI
app = FastAPI(title="Microservicio de Monitoreo y Analítica")

# --- BLOQUE DE CORS ELIMINADO ---
# El API Gateway (Puerto 8081) ahora gestiona el CORS para evitar duplicidad de headers.

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

# --- FUNCIONALIDADES DE REPORTES (SINCRONIZACIÓN DESDE FRONTEND) ---

@app.post("/api/analisis/reportes/periodico")
async def recolectar_datos_desde_frontend(
    datos_proyectos: List[dict], 
    db: Session = Depends(database.get_db)
):
    total_proyectos = len(datos_proyectos)
    proyectos_criticos = 0
    
    for p in datos_proyectos:
        id_p = p.get("id_proyecto")
        completadas = p.get("tareas_completadas", 0)
        totales = p.get("tareas_totales", 1)
        
        # Cálculo del avance
        avance = (completadas / totales) * 100
        
        if avance < 40:
            proyectos_criticos += 1
            
        # Preparamos el schema para la métrica
        metrica_data = schemas.MetricaCreate(
            id_proyecto=id_p,
            porcentaje_avance=avance,
            tareas_completadas=completadas,
            tareas_totales=totales
        )
        
        # INTEGRACIÓN: Usamos la lógica de "Actualizar o Crear" para evitar duplicados
        crud.update_or_create_metrica(db, metrica_data)
    
    # Generar el reporte de la sincronización (el historial de reportes sí se mantiene acumulativo)
    resumen_texto = f"Sincronización manual desde Front. {total_proyectos} proyectos procesados. {proyectos_criticos} críticos."
    estado = "Atención Requerida" if proyectos_criticos > 0 else "Estable"
    nuevo_reporte = schemas.ReporteCreate(resumen=resumen_texto, estado_general=estado)
    crud.create_reporte(db, nuevo_reporte)
    
    return {
        "status": "success", 
        "message": "Analítica actualizada con datos del frontend",
        "reporte_resumen": resumen_texto
    }

@app.get("/api/analisis/alertas")
async def detectar_alertas(db: Session = Depends(database.get_db)):
    metricas = crud.get_metricas(db)
    alertas = [m for m in metricas if m.porcentaje_avance < 40.0]
    return {"alertas_criticas": alertas}

# --- FUNCIÓN DE DASHBOARD Y REPORTES ---

@app.get("/api/analisis/dashboard", response_model=schemas.DashboardData)
def dashboard_consolidado(db: Session = Depends(database.get_db)):
    return {
        "kpis": crud.get_kpis(db),
        "metricas": crud.get_metricas(db),
        "reportes_recientes": crud.get_reportes(db)
    }

@app.get("/api/analisis/reportes", response_model=List[schemas.ReporteResponse])
def listar_reportes(db: Session = Depends(database.get_db)):
    return crud.get_reportes(db)

# --- CRUD MÉTRICAS DE PROYECTOS ---

@app.get("/api/analisis/metricas", response_model=List[schemas.MetricaResponse])
def listar_todas_metricas(db: Session = Depends(database.get_db)):
    return crud.get_metricas(db)

@app.get("/api/analisis/metrica/{id_metrica}", response_model=schemas.MetricaResponse)
def obtener_metrica_especifica(id_metrica: int, db: Session = Depends(database.get_db)):
    return crud.get_metrica(db, id_metrica)

@app.delete("/api/analisis/metrica/{id_metrica}")
def eliminar_metrica(id_metrica: int, db: Session = Depends(database.get_db)):
    crud.delete_metrica(db, id_metrica)
    return {"message": "Métrica eliminada"}