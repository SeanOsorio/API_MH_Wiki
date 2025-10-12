import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.weapons_model import Base
from dotenv import load_dotenv

load_dotenv()

# Variables globales para engine y session
engine = None
SessionLocal = None

def get_database_url():
    """
    🔗 Obtiene la URL de la base de datos con respaldo automático
    
    Prioridad:
    1. DATABASE_URL completa desde .env
    2. Parámetros individuales de PostgreSQL
    3. SQLite local como respaldo
    """
    
    # Opción 1: URL completa desde variable de entorno
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return database_url, "PostgreSQL (URL completa)"
    
    # Opción 2: Parámetros individuales de PostgreSQL
    dbuser = os.getenv('DBUSER')
    dbpassword = os.getenv('DBPASSWORD') 
    dbhost = os.getenv('DBHOST')
    dbport = os.getenv('DBPORT', '5432')
    dbname = os.getenv('DBNAME')
    
    if all([dbuser, dbpassword, dbhost, dbname]):
        return f"postgresql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}", "PostgreSQL (parámetros)"
    
    # Opción 3: SQLite local como respaldo
    db_dir = Path('data')
    db_dir.mkdir(exist_ok=True)  # Crear directorio si no existe
    sqlite_path = db_dir / 'parcial1web.db'
    return f"sqlite:///{sqlite_path}", "SQLite local"

def create_database_engine(database_url, db_type):
    """
    🏗️ Crea el engine de la base de datos con configuración optimizada
    """
    if 'sqlite' in database_url.lower():
        # Configuración para SQLite
        return create_engine(
            database_url,
            echo=False,  # Menos verbose para SQLite
            connect_args={"check_same_thread": False}  # Permitir múltiples threads
        )
    else:
        # Configuración para PostgreSQL
        return create_engine(
            database_url,
            echo=False,  # Menos verbose por defecto
            pool_pre_ping=True,  # Verificar conexión antes de usar
            pool_recycle=300     # Reciclar conexiones cada 5 minutos
        )

def test_database_connection(engine, db_type):
    """
    🧪 Prueba la conexión a la base de datos
    """
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()  # Confirmar que podemos leer
        return True
    except Exception as e:
        print(f"❌ Error de conexión ({db_type}): {e}")
        return False

def get_engine(custom_url=None):
    """
    🔧 Obtiene el engine de la base de datos (con lazy loading)
    """
    global engine
    
    if engine is None or custom_url:
        url_to_use = custom_url if custom_url else get_database_url()[0]
        engine = create_database_engine(url_to_use, "custom" if custom_url else "auto")
    
    return engine

def get_session_factory(custom_url=None):
    """
    🏭 Obtiene la factory de sesiones
    """
    global SessionLocal
    
    if SessionLocal is None or custom_url:
        engine_to_use = get_engine(custom_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_to_use)
    
    return SessionLocal

def get_db():
    """
    📦 Generador de sesiones de base de datos para dependency injection
    """
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    🚀 Inicialización inteligente de la base de datos
    
    Intenta conectar en orden de prioridad y usa SQLite como respaldo
    """
    global engine, SessionLocal
    
    print("🔍 Detectando configuración de base de datos...")
    
    # Obtener URL y tipo
    database_url, db_type = get_database_url()
    print(f"📋 Configuración detectada: {db_type}")
    print(f"🔗 URL: {database_url}")
    
    # Si es PostgreSQL, intentar conectar primero
    if 'postgresql' in database_url.lower():
        print("🔄 Intentando conectar a PostgreSQL...")
        postgres_engine = create_database_engine(database_url, db_type)
        
        if test_database_connection(postgres_engine, db_type):
            print("✅ Conexión a PostgreSQL exitosa")
            engine = postgres_engine
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        else:
            print("⚠️  No se pudo conectar a PostgreSQL, usando SQLite como respaldo...")
            
            # Usar SQLite como respaldo
            db_dir = Path('data')
            db_dir.mkdir(exist_ok=True)
            sqlite_path = db_dir / 'parcial1web.db'
            sqlite_url = f"sqlite:///{sqlite_path}"
            
            print(f"🔄 Configurando SQLite: {sqlite_url}")
            engine = create_database_engine(sqlite_url, "SQLite local")
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            
            if test_database_connection(engine, "SQLite"):
                print("✅ Base de datos SQLite configurada como respaldo")
            else:
                raise Exception("No se pudo configurar ninguna base de datos")
    
    else:
        # Ya es SQLite, usar directamente
        print("🔄 Configurando SQLite...")
        engine = create_database_engine(database_url, db_type)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        if test_database_connection(engine, db_type):
            print("✅ Base de datos SQLite configurada")
        else:
            raise Exception("No se pudo configurar la base de datos SQLite")
    
    # Crear todas las tablas
    print("📋 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas/verificadas correctamente")
    
    return True