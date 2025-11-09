"""
Script para crear el primer usuario administrador del sistema.
Solo se ejecuta una vez durante la configuración inicial.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.auth_service import register_user, hash_password
from models.user_model import UserRole
from repositories.user_repository import UserRepository

def create_admin():
    """Crea el primer usuario administrador."""
    
    print("=" * 70)
    print("👑 CREAR PRIMER ADMINISTRADOR")
    print("=" * 70)
    print()
    
    user_repo = UserRepository()
    
    # Verificar si ya existe un admin
    admin_count = user_repo.count_admins()
    
    if admin_count > 0:
        print(f"⚠️  Ya existen {admin_count} administrador(es) en el sistema")
        print()
        response = input("¿Deseas crear otro administrador? (s/n): ").lower()
        if response != 's':
            print("❌ Operación cancelada")
            return
        print()
    
    # Solicitar datos
    print("Ingresa los datos del administrador:")
    print()
    
    username = input("👤 Username (min 3 caracteres): ").strip()
    email = input("📧 Email: ").strip()
    password = input("🔐 Password (min 6 caracteres): ").strip()
    
    if not username or not email or not password:
        print("\n❌ Error: Todos los campos son requeridos")
        return
    
    # Confirmar password
    password_confirm = input("🔐 Confirmar password: ").strip()
    
    if password != password_confirm:
        print("\n❌ Error: Las contraseñas no coinciden")
        return
    
    print()
    
    # Crear usuario admin
    user, error = register_user(username, email, password, UserRole.ADMIN)
    
    if error:
        print(f"❌ Error: {error}")
        return
    
    print("=" * 70)
    print("✅ ADMINISTRADOR CREADO EXITOSAMENTE")
    print("=" * 70)
    print()
    print(f"👤 Username: {user.username}")
    print(f"📧 Email: {user.email}")
    print(f"👑 Rol: {user.role.value}")
    print(f"📅 Creado: {user.created_at}")
    print()
    print("💡 Ahora puedes iniciar sesión con estas credenciales en:")
    print("   POST /api/auth/login")
    print()


if __name__ == '__main__':
    try:
        create_admin()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
