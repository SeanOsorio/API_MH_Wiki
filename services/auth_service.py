# -*- coding: utf-8 -*-
"""
🔐 SERVICIO DE AUTENTICACIÓN Y ROLES
==================================
Maneja usuarios, roles, permisos y autenticación JWT
"""

import json
import secrets
from typing import Dict, Any
from datetime import datetime, timedelta
from config.database import get_db
from models.weapons_model import User, Role, RefreshToken
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token

bcrypt = Bcrypt()

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña contra su hash
    """
    return bcrypt.check_password_hash(hashed_password, password)

# ==========================================
# 👤 GESTIÓN DE USUARIOS
# ==========================================

def create_user(username, email, password, role_name="user"):
    """Crear un nuevo usuario con rol específico"""
    db = next(get_db())
    
    # Verificar si ya existe el usuario
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        return None, "Usuario o email ya existe"
    
    # Obtener el rol
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        return None, f"Rol '{role_name}' no existe"
    
    # Crear usuario
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role_id=role.id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user, "Usuario creado exitosamente"

def register_user(username: str, email: str, password: str, role_name: str = "user") -> Dict[str, Any]:
    """
    Registra un nuevo usuario con rol
    """
    db = next(get_db())
    try:
        # Verificar si el email o username ya existe
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            return {'success': False, 'message': 'El email o username ya está registrado'}
        
        # Obtener el rol (por defecto 'user')
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = db.query(Role).filter(Role.name == 'user').first()
        
        # Crear nuevo usuario
        password_hash = hash_password(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role_id=role.id if role else 2  # Default role ID
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            'success': True,
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'role': role.name if role else 'user',
                'created_at': new_user.created_at.isoformat()
            }
        }
    
    except Exception as e:
        db.rollback()
        return {'success': False, 'message': f'Error al registrar usuario: {str(e)}'}
    
    finally:
        db.close()

def authenticate_user(username, password):
    """Autenticar usuario por username o email"""
    db = next(get_db())
    
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return user
    return None

def login_user(username: str, password: str) -> Dict[str, Any]:
    """
    Autentica un usuario y genera tokens JWT (access y refresh)
    """
    db = next(get_db())
    try:
        # Buscar usuario por username o email
        user = db.query(User).filter(
            ((User.username == username) | (User.email == username)) & (User.is_active == True)
        ).first()
        
        if not user or not verify_password(password, user.password_hash):
            return {'success': False, 'message': 'Credenciales inválidas'}
        
        # Crear tokens JWT con información del rol
        additional_claims = {
            'role': user.role.name if user.role else 'user',
            'permissions': json.loads(user.role.permissions) if user.role and user.role.permissions else []
        }
        
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=1)
        )
        
        refresh_token_jwt = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)  # Refresh token dura 30 días
        )
        
        # Guardar refresh token en la base de datos
        refresh_token_record = RefreshToken(
            token=refresh_token_jwt,
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        
        db.add(refresh_token_record)
        db.commit()
        
        return {
            'success': True,
            'access_token': access_token,
            'refresh_token': refresh_token_jwt,
            'expires_in': 3600,  # Access token expira en 1 hora
            'refresh_expires_in': 2592000,  # Refresh token expira en 30 días
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.name if user.role else 'user'
            }
        }
    
    except Exception as e:
        db.rollback()
        return {'success': False, 'message': f'Error en el login: {str(e)}'}
    
    finally:
        db.close()

def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
    """
    Genera un nuevo access token usando un refresh token válido
    """
    db = next(get_db())
    try:
        # Buscar el refresh token en la base de datos
        token_record = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()
        
        if not token_record:
            return {'success': False, 'message': 'Refresh token inválido o expirado'}
        
        # Verificar que el usuario aún esté activo
        user = db.query(User).filter(
            User.id == token_record.user_id,
            User.is_active == True
        ).first()
        
        if not user:
            return {'success': False, 'message': 'Usuario no válido'}
        
        # Crear nuevo access token
        new_access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1)
        )
        
        return {
            'success': True,
            'access_token': new_access_token,
            'expires_in': 3600  # 1 hora en segundos
        }
    
    except Exception as e:
        return {'success': False, 'message': f'Error al refrescar token: {str(e)}'}
    
    finally:
        db.close()

def revoke_refresh_token(refresh_token: str) -> Dict[str, Any]:
    """
    Revoca un refresh token específico
    """
    db = next(get_db())
    try:
        # Buscar y revocar el refresh token
        token_record = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.is_revoked == False
        ).first()
        
        if token_record:
            token_record.is_revoked = True
            db.commit()
            return {'success': True, 'message': 'Token revocado exitosamente'}
        else:
            return {'success': False, 'message': 'Token no encontrado'}
    
    except Exception as e:
        db.rollback()
        return {'success': False, 'message': f'Error al revocar token: {str(e)}'}
    
    finally:
        db.close()

def revoke_all_user_tokens(user_id: int) -> Dict[str, Any]:
    """
    Revoca todos los refresh tokens de un usuario
    """
    db = next(get_db())
    try:
        revoked_count = db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).update({'is_revoked': True})
        
        db.commit()
        return {
            'success': True, 
            'message': f'Se revocaron {revoked_count} tokens exitosamente'
        }
    
    except Exception as e:
        db.rollback()
        return {'success': False, 'message': f'Error al revocar tokens: {str(e)}'}
    
    finally:
        db.close()

def cleanup_expired_tokens() -> int:
    """
    Limpia tokens expirados de la base de datos
    """
    db = next(get_db())
    try:
        # Eliminar tokens expirados
        expired_count = db.query(RefreshToken).filter(
            RefreshToken.expires_at < datetime.utcnow()
        ).delete()
        
        db.commit()
        return expired_count
    
    except Exception as e:
        db.rollback()
        return 0
    
    finally:
        db.close()

def get_user_by_id(user_id: int) -> User:
    """
    Obtiene un usuario por su ID
    """
    db = next(get_db())
    try:
        return db.query(User).filter(User.id == user_id, User.is_active == True).first()
    finally:
        db.close()

def get_user_with_role(user_id):
    """Obtener usuario con información completa del rol"""
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.role:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'role': {
                'id': user.role.id,
                'name': user.role.name,
                'description': user.role.description,
                'permissions': json.loads(user.role.permissions) if user.role.permissions else []
            }
        }
    return None

def update_user_role(user_id, role_name):
    """Cambiar el rol de un usuario"""
    db = next(get_db())
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None, "Usuario no encontrado"
    
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        return None, f"Rol '{role_name}' no existe"
    
    user.role_id = role.id
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return user, f"Rol cambiado a '{role_name}'"

def get_all_users():
    """Obtener todos los usuarios con sus roles"""
    db = next(get_db())
    users = db.query(User).all()
    
    result = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'role': {
                'id': user.role.id,
                'name': user.role.name,
                'description': user.role.description
            } if user.role else None
        }
        result.append(user_data)
    
    return result

# ==========================================
# 🛡️ GESTIÓN DE ROLES Y PERMISOS
# ==========================================

def create_role(name, description, permissions):
    """Crear un nuevo rol con permisos específicos"""
    db = next(get_db())
    
    existing_role = db.query(Role).filter(Role.name == name).first()
    if existing_role:
        return None, "El rol ya existe"
    
    permissions_json = json.dumps(permissions) if isinstance(permissions, list) else permissions
    
    new_role = Role(
        name=name,
        description=description,
        permissions=permissions_json
    )
    
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return new_role, "Rol creado exitosamente"

def get_all_roles():
    """Obtener todos los roles disponibles"""
    db = next(get_db())
    roles = db.query(Role).filter(Role.is_active == True).all()
    
    result = []
    for role in roles:
        role_data = {
            'id': role.id,
            'name': role.name,
            'description': role.description,
            'permissions': json.loads(role.permissions) if role.permissions else [],
            'user_count': len(role.users)
        }
        result.append(role_data)
    
    return result

def get_role_by_name(role_name):
    """Obtener rol específico por nombre"""
    db = next(get_db())
    return db.query(Role).filter(Role.name == role_name).first()

def user_has_permission(user_id, permission):
    """Verificar si un usuario tiene un permiso específico"""
    user = get_user_by_id(user_id)
    if not user or not user.role:
        return False
    
    if not user.role.permissions:
        return False
    
    permissions = json.loads(user.role.permissions)
    return permission in permissions or 'admin' in permissions

def user_has_role(user_id, role_name):
    """Verificar si un usuario tiene un rol específico"""
    user = get_user_by_id(user_id)
    if not user or not user.role:
        return False
    
    return user.role.name == role_name

# ==========================================
# 🔄 GESTIÓN DE REFRESH TOKENS (Actualizada)
# ==========================================

def create_refresh_token_record(user_id, token_value, expires_at):
    """Crear un nuevo refresh token"""
    db = next(get_db())
    
    refresh_token = RefreshToken(
        token=token_value,
        user_id=user_id,
        expires_at=expires_at
    )
    
    db.add(refresh_token)
    db.commit()
    
    return refresh_token

def get_refresh_token(token_value):
    """Obtener refresh token por valor"""
    db = next(get_db())
    return db.query(RefreshToken).filter(
        RefreshToken.token == token_value,
        RefreshToken.is_revoked == False,
        RefreshToken.expires_at > datetime.utcnow()
    ).first()

# ==========================================
# 🏗️ INICIALIZACIÓN DE ROLES POR DEFECTO
# ==========================================

def initialize_default_roles():
    """Crear roles por defecto si no existen"""
    db = next(get_db())
    
    # Definir roles por defecto
    default_roles = [
        {
            'name': 'admin',
            'description': 'Administrador del sistema con todos los permisos',
            'permissions': [
                'admin',                    # Permiso especial de administrador
                'user_management',          # Gestionar usuarios
                'role_management',          # Gestionar roles
                'weapon_create',           # Crear armas
                'weapon_read',             # Leer armas
                'weapon_update',           # Actualizar armas
                'weapon_delete',           # Eliminar armas
                'category_create',         # Crear categorías
                'category_read',           # Leer categorías
                'category_update',         # Actualizar categorías
                'category_delete'          # Eliminar categorías
            ]
        },
        {
            'name': 'user',
            'description': 'Usuario estándar con permisos básicos',
            'permissions': [
                'weapon_read',             # Solo leer armas
                'category_read'            # Solo leer categorías
            ]
        },
        {
            'name': 'moderator',
            'description': 'Moderador con permisos de gestión limitados',
            'permissions': [
                'weapon_create',           # Crear armas
                'weapon_read',             # Leer armas
                'weapon_update',           # Actualizar armas
                'category_create',         # Crear categorías
                'category_read',           # Leer categorías
                'category_update'          # Actualizar categorías
            ]
        }
    ]
    
    created_roles = []
    for role_data in default_roles:
        existing_role = db.query(Role).filter(Role.name == role_data['name']).first()
        
        if not existing_role:
            permissions_json = json.dumps(role_data['permissions'])
            new_role = Role(
                name=role_data['name'],
                description=role_data['description'],
                permissions=permissions_json
            )
            db.add(new_role)
            created_roles.append(role_data['name'])
    
    if created_roles:
        db.commit()
    
    return created_roles

def create_admin_user():
    """Crear usuario administrador por defecto"""
    db = next(get_db())
    
    # Verificar si ya existe un admin
    admin_user = db.query(User).join(Role).filter(Role.name == 'admin').first()
    
    if not admin_user:
        # Crear usuario admin por defecto
        admin_role = db.query(Role).filter(Role.name == 'admin').first()
        if admin_role:
            password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin_user = User(
                username='admin',
                email='admin@parcial1web.com',
                password_hash=password_hash,
                role_id=admin_role.id
            )
            db.add(admin_user)
            db.commit()
            return admin_user
    
    return admin_user