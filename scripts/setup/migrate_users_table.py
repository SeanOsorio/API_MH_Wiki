"""
Migración para crear la tabla de usuarios.
Ejecuta este script UNA VEZ para agregar la tabla users a Railway.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import engine
from sqlalchemy import text

def create_users_table():
    """Crea la tabla de usuarios en PostgreSQL."""
    
    print("=" * 70)
    print("🔐 CREANDO TABLA DE USUARIOS")
    print("=" * 70)
    print()
    
    with engine.connect() as conn:
        try:
            # Crear tipo enum para roles
            print("📝 Paso 1: Creando tipo enum userrole...")
            conn.execute(text("""
                DO $$ BEGIN
                    CREATE TYPE userrole AS ENUM ('user', 'admin');
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            """))
            conn.commit()
            print("   ✅ Tipo userrole creado\n")
            
            # Crear tabla users
            print("📝 Paso 2: Creando tabla users...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role userrole NOT NULL DEFAULT 'user',
                    is_active BOOLEAN NOT NULL DEFAULT true,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP WITH TIME ZONE
                );
            """))
            conn.commit()
            print("   ✅ Tabla users creada\n")
            
            # Crear índices
            print("📝 Paso 3: Creando índices...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            """))
            conn.commit()
            print("   ✅ Índices creados\n")
            
            print("=" * 70)
            print("✅ TABLA DE USUARIOS CREADA EXITOSAMENTE")
            print("=" * 70)
            print()
            print("💡 Próximos pasos:")
            print("   1. Ejecuta: python create_admin.py")
            print("   2. Crea tu primer usuario administrador")
            print("   3. Inicia el servidor: python app.py")
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            conn.rollback()
            raise


if __name__ == '__main__':
    try:
        create_users_table()
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
