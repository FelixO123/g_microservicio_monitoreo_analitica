import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas, models

# --- CONFIGURACIÓN DE LA BASE DE DATOS DE PRUEBA ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    # Crea las tablas antes de cada prueba
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    # Limpia todo después de cada prueba
    session.close()
    Base.metadata.drop_all(bind=engine)

# --- PRUEBAS UNITARIAS: CRUD KPI ---

def test_kpi_full_cycle(db):
    # 1. Create
    kpi_in = schemas.KPICreate(nombre="Disponibilidad", descripcion="Server Up", valor=99.9)
    db_kpi = crud.create_kpi(db, kpi_in)
    assert db_kpi.id_kpi is not None
    assert db_kpi.nombre == "Disponibilidad"

    # 2. Get All
    kpis = crud.get_kpis(db)
    assert len(kpis) == 1

    # 3. Get One
    found = crud.get_kpi(db, db_kpi.id_kpi)
    assert found.id_kpi == db_kpi.id_kpi

    # 4. Update
    update_data = schemas.KPICreate(nombre="Actualizado", descripcion="Nueva desc", valor=80.0)
    updated = crud.update_kpi(db, db_kpi.id_kpi, update_data)
    assert updated.nombre == "Actualizado"
    assert updated.valor == 80.0

    # 5. Delete
    crud.delete_kpi(db, db_kpi.id_kpi)
    assert crud.get_kpi(db, db_kpi.id_kpi) is None


# --- PRUEBAS UNITARIAS: CRUD REPORTES ---

def test_reporte_full_cycle(db):
    # 1. Create
    repo_in = schemas.ReporteCreate(resumen="Resumen Inicial", estado_general="Estable")
    db_repo = crud.create_reporte(db, repo_in)
    assert db_repo.id_reporte is not None

    # 2. Get All
    reportes = crud.get_reportes(db)
    assert len(reportes) == 1
    
    # 3. Get One (NUEVA PRUEBA)
    found = crud.get_reporte(db, reporte_id=db_repo.id_reporte)
    assert found is not None
    assert found.id_reporte == db_repo.id_reporte
    assert found.resumen == "Resumen Inicial"

    # 4. Update
    update_data = schemas.ReporteCreate(resumen="Resumen Editado", estado_general="Crítico")
    updated = crud.update_reporte(db, db_repo.id_reporte, update_data)
    assert updated.estado_general == "Crítico"

    # 5. Delete
    crud.delete_reporte(db, db_repo.id_reporte)
    # Verificación manual en la DB de que se borró
    check = db.query(models.Reporte).filter(models.Reporte.id_reporte == db_repo.id_reporte).first()
    assert check is None


# --- PRUEBAS UNITARIAS: CRUD MÉTRICAS ---

def test_metrica_full_cycle(db):
    # 1. Create
    metrica_in = schemas.MetricaCreate(
        id_proyecto=101, 
        porcentaje_avance=45.5, 
        tareas_completadas=4, 
        tareas_totales=10
    )
    db_metrica = crud.create_metrica(db, metrica_in)
    assert db_metrica.id_metrica is not None

    # 2. Get All
    metricas = crud.get_metricas(db)
    assert len(metricas) == 1

    # 3. Get Specific
    found = crud.get_metrica(db, db_metrica.id_metrica)
    assert found.id_proyecto == 101

    # 4. Get By Project (Retorna Lista según tu crud.py)
    by_project = crud.get_metrica_por_proyecto(db, 101)
    assert isinstance(by_project, list)
    assert by_project[0].porcentaje_avance == 45.5

    # 5. Update
    update_data = schemas.MetricaCreate(
        id_proyecto=101, porcentaje_avance=100.0, tareas_completadas=10, tareas_totales=10
    )
    updated = crud.update_metrica(db, db_metrica.id_metrica, update_data)
    assert updated.porcentaje_avance == 100.0

    # 6. Delete
    crud.delete_metrica(db, db_metrica.id_metrica)
    assert crud.get_metrica(db, db_metrica.id_metrica) is None