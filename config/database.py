"""
Configuración de base de datos para la API de Monster Hunter Weapons.

Este módulo maneja:
- Conexión a PostgreSQL en Railway usando variables de entorno
- Creación del motor SQLAlchemy con configuraciones optimizadas
- Gestión de sesiones de base de datos con context manager
- Inicialización automática de tablas

Variables de entorno requeridas:
- DBUSER: Usuario de la base de datos
- DBPASSWORD: Contraseña del usuario
- DBHOST: Host del servidor PostgreSQL
- DBPORT: Puerto (por defecto 5432)
- DBNAME: Nombre de la base de datos
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.weapons_model import Base
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener credenciales de base de datos desde variables de entorno
DBUSER = os.getenv('DBUSER')
DBPASSWORD = os.getenv('DBPASSWORD') 
DBHOST = os.getenv('DBHOST')
DBPORT = os.getenv('DBPORT', '5432')
DBNAME = os.getenv('DBNAME')

# Validar que todas las variables requeridas estén presentes
required_vars = ['DBUSER', 'DBPASSWORD', 'DBHOST', 'DBNAME']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise ValueError(f"Variables de entorno faltantes: {', '.join(missing_vars)}")

# Construir URL de conexión para PostgreSQL
DATABASE_URL = f"postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"

# Crear motor SQLAlchemy con configuraciones para producción
engine = create_engine(
    DATABASE_URL, 
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600,
    max_overflow=20,
    pool_size=10
)

# Configurar factory de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    Generador de sesiones de base de datos con context manager.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas.
    """
    print(" Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print(" Tablas creadas/verificadas correctamente")
