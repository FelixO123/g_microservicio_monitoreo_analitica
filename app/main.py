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

