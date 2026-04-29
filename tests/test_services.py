import pytest
from app import services
from fastapi import HTTPException

# Configuramos pytest para que maneje funciones asíncronas automáticamente
pytestmark = pytest.mark.asyncio

# --- PRUEBAS PARA DATOS FICTICIOS (ESTADO ACTUAL) ---

async def test_obtener_datos_proyectos_ficticios():
    """Valida que la función devuelva la lista de proyectos estática correctamente"""
    resultado = await services.obtener_datos_proyectos()
    assert isinstance(resultado, list)
    assert len(resultado) == 2
    assert resultado[0]["nombre"] == "Sistema E-commerce"

async def test_obtener_carga_trabajo_ficticia():
    """Valida que la función devuelva la carga de trabajo estática correctamente"""
    resultado = await services.obtener_carga_trabajo()
    assert isinstance(resultado, list)
    assert len(resultado) == 2
    assert resultado[0]["id_usuario"] == 1

# --- PRUEBAS DE ESTRUCTURA (ATRIBUTOS ESPECÍFICOS) ---

async def test_obtener_datos_proyectos_estructura():
    """Valida que los diccionarios de proyectos tengan las llaves correctas"""
    resultado = await services.obtener_datos_proyectos()
    # Atributos que definiste en tu services.py
    campos_esperados = {"id_proyecto", "nombre", "tareas_completadas", "tareas_totales"}
    for proyecto in resultado:
        assert campos_esperados.issubset(proyecto.keys())

async def test_obtener_carga_trabajo_estructura():
    """Valida que los diccionarios de carga de trabajo tengan las llaves correctas"""
    resultado = await services.obtener_carga_trabajo()
    # Atributos que definiste en tu services.py
    campos_esperados = {"id_carga", "id_usuario", "horas_asignadas", "periodo"}
    for carga in resultado:
        assert campos_esperados.issubset(carga.keys())

# --- PRUEBAS DE "MOCKING" (ERRORES DE RED) ---

async def test_obtener_datos_proyectos_error_red(mocker):
    """Simula un error de conexión en el microservicio de Proyectos"""
    mocker.patch("httpx.AsyncClient.get", side_effect=Exception("Timeout"))
    resultado = await services.obtener_datos_proyectos()
    assert isinstance(resultado, list) # Valida que el código sigue vivo

async def test_obtener_carga_trabajo_error_red(mocker):
    """Simula un error de conexión en el microservicio de Usuarios"""
    mocker.patch("httpx.AsyncClient.get", side_effect=Exception("Connection Refused"))
    resultado = await services.obtener_carga_trabajo()
    assert isinstance(resultado, list)