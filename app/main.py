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

# --- FUNCION DE CRUD UTILIZACION DE PERSONAL ---

@app.get("/api/analisis/ocupacion")
async def mostrar_ocupacion_personal():
    return await services.obtener_carga_trabajo()

@app.get("/api/analisis/ocupacion/{id_usuario}")
async def ocupacion_usuario_especifico(id_usuario: int):
    cargas = await services.obtener_carga_trabajo()
    usuario = next((c for c in cargas if c["id_usuario"] == id_usuario), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Carga de usuario no encontrada")
    return usuario

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