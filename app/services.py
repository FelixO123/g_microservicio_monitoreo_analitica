import httpx
import os
from fastapi import HTTPException
from dotenv import load_dotenv

# Cargamos las variables del .env que está en la raíz
load_dotenv()

# Obtenemos las URLs de producción
URL_PROYECTOS = os.getenv("MS_PROYECTOS_URL")
URL_USUARIOS = os.getenv("MS_USUARIOS_URL")

# --- SERVICIOS PARA PROYECTOS (Reportes y Alertas) ---

async def obtener_datos_proyectos():
    """
    Obtiene la lista de proyectos. 
    Sirve para: POST /api/analisis/reportes/periodico y GET /api/analisis/alertas
    """
    
    # =====================================================
    # BLOQUE 1: DATOS FICTICIOS (ACTIVO PARA PRUEBAS)
    # =====================================================
    return [
        {
            "id_proyecto": 1, 
            "nombre": "Sistema E-commerce", 
            "tareas_completadas": 2, 
            "tareas_totales": 10  # 20% avance -> ACTIVARÁ ALERTA
        },
        {
            "id_proyecto": 5, 
            "nombre": "App Móvil Delivery", 
            "tareas_completadas": 8, 
            "tareas_totales": 10  # 80% avance -> ESTADO ESTABLE
        }
    ]
    
    # =====================================================
    # BLOQUE 2: LÓGICA REAL (DESCOMENTAR PARA PRODUCCIÓN)
    # =====================================================
    """
    if not URL_PROYECTOS:
        raise HTTPException(status_code=500, detail="URL de MS Proyectos no configurada")
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.get(f"{URL_PROYECTOS}/api/proyectos")
            response.raise_for_status() 
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, 
                detail=f"Error en MS Proyectos: {e.response.text}"
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=503, 
                detail="Servicio de Proyectos en la nube no alcanzable"
            )
    """
