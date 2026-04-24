import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env que está en la raíz
load_dotenv()

# Obtenemos la URL de la base de datos desde el .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Verificación de seguridad por si el .env no se carga correctamente
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("La variable DATABASE_URL no está definida en el archivo .env")

# Configuración del motor (Engine)
# pool_pre_ping=True es vital para conexiones con Neon (evita desconexiones por inactividad)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

# Sesión local para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos de SQLAlchemy
Base = declarative_base()

# Dependencia para FastAPI (Inyección de dependencias)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()