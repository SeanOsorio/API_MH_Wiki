"""
Script de prueba de conexión a PostgreSQL en Railway
"""

from config.database import engine, init_db
from sqlalchemy import text

print("=" * 60)
print("🔌 PROBANDO CONEXIÓN A POSTGRESQL EN RAILWAY")
print("=" * 60)

try:
    # Probar conexión básica
    print("\n1️⃣ Probando conexión básica...")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ Conexión exitosa!")
        print(f"📊 PostgreSQL version: {version[:50]}...")
    
    # Inicializar tablas
    print("\n2️⃣ Inicializando tablas...")
    init_db()
    
    # Verificar tablas creadas
    print("\n3️⃣ Verificando tablas creadas...")
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
        tables = result.fetchall()
        
        if tables:
            print("✅ Tablas en la base de datos:")
            for table in tables:
                print(f"   • {table[0]}")
        else:
            print("⚠️ No se encontraron tablas")
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("=" * 60)
    print("\n🎮 La base de datos está lista para Monster Hunter Weapons API!")
    
except Exception as e:
    print("\n" + "=" * 60)
    print(f"❌ ERROR: {str(e)}")
    print("=" * 60)
    print("\n💡 Verifica:")
    print("   1. Las credenciales en el archivo .env")
    print("   2. Que el servidor de Railway esté accesible")
    print("   3. Que psycopg2-binary esté instalado")
