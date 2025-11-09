import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales de base de datos
db_host = os.getenv('DBHOST')
db_port = os.getenv('DBPORT')
db_name = os.getenv('DBNAME')
db_user = os.getenv('DBUSER')
db_password = os.getenv('DBPASSWORD')

def clear_database():
    """Limpiar todos los datos de las tablas"""
    connection = None
    cursor = None
    
    try:
        # Conectar a la base de datos
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        cursor = connection.cursor()
        
        print("🔗 Conectado a la base de datos")
        
        # Deshabilitar verificación de claves foráneas temporalmente
        cursor.execute("SET session_replication_role = 'replica';")
        
        # Limpiar tabla de armas (primero por la clave foránea)
        cursor.execute("DELETE FROM weapons;")
        weapons_deleted = cursor.rowcount
        print(f"🗑️  Eliminadas {weapons_deleted} armas")
        
        # Limpiar tabla de categorías
        cursor.execute("DELETE FROM weapon_categories;")
        categories_deleted = cursor.rowcount
        print(f"🗑️  Eliminadas {categories_deleted} categorías")
        
        # Reiniciar las secuencias de auto-incremento
        cursor.execute("ALTER SEQUENCE weapon_categories_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE weapons_id_seq RESTART WITH 1;")
        print("🔄 Secuencias de ID reiniciadas")
        
        # Rehabilitar verificación de claves foráneas
        cursor.execute("SET session_replication_role = 'origin';")
        
        # Confirmar cambios
        connection.commit()
        
        print("✅ Base de datos limpiada exitosamente")
        print("📊 Todas las tablas están vacías y listas para nuevos datos")
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"❌ Error al limpiar la base de datos: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("🔒 Conexión cerrada")

if __name__ == '__main__':
    print("⚠️  ADVERTENCIA: Esto eliminará TODOS los datos de la base de datos")
    confirm = input("¿Estás seguro de que quieres continuar? (escribe 'SI' para confirmar): ")
    
    if confirm == 'SI':
        clear_database()
    else:
        print("❌ Operación cancelada")
