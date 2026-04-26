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


# --- FUNCIONALIDADES DE REPORTES Y ALERTAS ---

@app.post("/api/analisis/reportes/periodico")
async def recolectar_datos_periodicos(db: Session = Depends(database.get_db)):
    # 1. Obtenemos datos de los otros microservicios
    proyectos = await services.obtener_datos_proyectos()
    
    total_proyectos = len(proyectos)
    proyectos_criticos = 0
    
    # 2. Procesamos cada proyecto y creamos su métrica
    for p in proyectos:
        completadas = p.get("tareas_completadas", 0)
        totales = p.get("tareas_totales", 1)
        avance = (completadas / totales) * 100
        
        if avance < 40:
            proyectos_criticos += 1
            
        metrica_data = schemas.MetricaCreate(
            id_proyecto=p["id_proyecto"],
            porcentaje_avance=avance,
            tareas_completadas=completadas,
            tareas_totales=totales
        )
        # Guardamos la métrica individual
        crud.create_metrica(db, metrica_data)
    
    # 3. AQUÍ ESTÁ LO QUE FALTA: Crear el registro en la entidad Reportes
    resumen_texto = (
        f"Sincronización exitosa. Se procesaron {total_proyectos} proyectos. "
        f"Se detectaron {proyectos_criticos} proyectos con avance crítico."
    )
    
    estado = "Atención Requerida" if proyectos_criticos > 0 else "Estable"
    
    nuevo_reporte = schemas.ReporteCreate(
        resumen=resumen_texto,
        estado_general=estado
    )
    
    # Guardamos el reporte en la base de datos
    crud.create_reporte(db, nuevo_reporte)
    
    return {
        "status": "success", 
        "message": "Métricas actualizadas y reporte generado",
        "reporte_resumen": resumen_texto
    }

@app.get("/api/analisis/alertas")
async def detectar_alertas(db: Session = Depends(database.get_db)):
    metricas = crud.get_metricas(db)
    # Lógica: detecta proyectos con menos del 40% de avance
    alertas = [m for m in metricas if m.porcentaje_avance < 40.0]
    return {"alertas_criticas": alertas}


# --- FUNCION DE DASHBOARD Y REPORTES ---

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

@app.post("/api/analisis/reportes", response_model=schemas.ReporteResponse)
def generar_nuevo_reporte(reporte: schemas.ReporteCreate, db: Session = Depends(database.get_db)):
    return crud.create_reporte(db, reporte)

@app.put("/api/analisis/reportes/{id_reportes}", response_model=schemas.ReporteResponse)
def actualizar_reporte(id_reportes: int, reporte: schemas.ReporteCreate, db: Session = Depends(database.get_db)):
    return crud.update_reporte(db, id_reportes, reporte)

@app.delete("/api/analisis/reportes/{id_reportes}")
def eliminar_reporte(id_reportes: int, db: Session = Depends(database.get_db)):
    db_reporte = crud.delete_reporte(db, id_reportes)
    if not db_reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return {"message": f"Reporte {id_reportes} eliminado correctamente"}

