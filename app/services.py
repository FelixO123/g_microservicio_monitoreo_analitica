import httpx
import os
from fastapi import HTTPException
from dotenv import load_dotenv

# Cargamos las variables del .env que está en la raíz
load_dotenv()

# Obtenemos las URLs de producción
URL_PROYECTOS = os.getenv("MS_PROYECTOS_URL")
URL_USUARIOS = os.getenv("MS_USUARIOS_URL")

# --- SERVICIOS PARA USUARIOS (Ocupación de Personal) ---

async def obtener_carga_trabajo():
    """
    Obtiene la carga de trabajo de los usuarios.
    Sirve para: GET /api/analisis/ocupacion y GET /api/analisis/ocupacion/{id_usuario}
    """

    # =====================================================
    # BLOQUE 1: DATOS FICTICIOS (ACTIVO PARA PRUEBAS)
    # =====================================================
    return [
        {
            "id_carga": 10,
            "id_usuario": 1,
            "horas_asignadas": 45,
            "periodo": "Mayo 2024"
        },
        {
            "id_carga": 11,
            "id_usuario": 2,
            "horas_asignadas": 20,
            "periodo": "Mayo 2024"
        }
    ]

    # =====================================================
    # BLOQUE 2: LÓGICA REAL (DESCOMENTAR PARA PRODUCCIÓN)
    # =====================================================
    """
    if not URL_USUARIOS:
        raise HTTPException(status_code=500, detail="URL de MS Usuarios no configurada")

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.get(f"{URL_USUARIOS}/api/usuarios/carga")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, 
                detail=f"Error en MS Usuarios: {e.response.text}"
            )
        except Exception:
            raise HTTPException(
                status_code=503, 
                detail="Servicio de Usuarios en la nube no alcanzable"
            )
    """