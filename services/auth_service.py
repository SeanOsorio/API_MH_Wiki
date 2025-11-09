"""
Servicio de autenticación con JWT y bcrypt.
Maneja registro, login, verificación de tokens y roles.
"""

import jwt
import os
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from functools import wraps
from flask import request, jsonify
from repositories.user_repository import UserRepository
from models.user_model import UserRole

# Inicializar bcrypt
bcrypt = Bcrypt()

# Configuración JWT
JWT_SECRET = os.getenv('JWT_SECRET', 'mh-wilds-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

user_repo = UserRepository()


def hash_password(password):
    """
    Hashea una contraseña usando bcrypt.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Contraseña hasheada
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')


def verify_password(password_hash, password):
    """
    Verifica que una contraseña coincida con el hash.
    
    Args:
        password_hash: Hash almacenado
        password: Contraseña a verificar
        
    Returns:
        bool: True si coincide, False si no
    """
    return bcrypt.check_password_hash(password_hash, password)


def generate_token(user_id, username, role):
    """
    Genera un token JWT para un usuario.
    
    Args:
        user_id: ID del usuario
        username: Nombre de usuario
        role: Rol del usuario
        
    Returns:
        str: Token JWT
    """
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    """
    Decodifica y verifica un token JWT.
    
    Args:
        token: Token JWT
        
    Returns:
        dict: Payload del token o None si es inválido
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def register_user(username, email, password, role=UserRole.USER):
    """
    Registra un nuevo usuario en el sistema.
    
    Args:
        username: Nombre de usuario
        email: Email del usuario
        password: Contraseña en texto plano
        role: Rol del usuario (por defecto USER)
        
    Returns:
        tuple: (usuario_creado, mensaje_error)
    """
    # Validaciones
    if not username or len(username) < 3:
        return None, "El nombre de usuario debe tener al menos 3 caracteres"
    
    if not email or '@' not in email:
        return None, "Email inválido"
    
    if not password or len(password) < 6:
        return None, "La contraseña debe tener al menos 6 caracteres"
    
    # Verificar si ya existe
    if user_repo.exists_by_username_or_email(username, email):
        return None, "El usuario o email ya están registrados"
    
    # Crear usuario
    user_data = {
        'username': username,
        'email': email,
        'password_hash': hash_password(password),
        'role': role
    }
    
    user = user_repo.create(user_data)
    return user, None


def login_user(username, password):
    """
    Autentica a un usuario y genera un token.
    
    Args:
        username: Nombre de usuario o email
        password: Contraseña
        
    Returns:
        tuple: (token, usuario, mensaje_error)
    """
    # Buscar usuario por username o email
    user = user_repo.get_by_username(username)
    if not user:
        user = user_repo.get_by_email(username)
    
    if not user:
        return None, None, "Usuario no encontrado"
    
    if not user.is_active:
        return None, None, "Usuario desactivado"
    
    # Verificar contraseña
    if not verify_password(user.password_hash, password):
        return None, None, "Contraseña incorrecta"
    
    # Actualizar último login
    user_repo.update_last_login(user.id)
    
    # Generar token
    token = generate_token(user.id, user.username, user.role.value)
    
    return token, user, None


# Decoradores para proteger rutas
def token_required(f):
    """
    Decorador para requerir token JWT en endpoints.
    Añade el payload del token a los argumentos de la función.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Buscar token en headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # "Bearer <token>"
            except IndexError:
                return jsonify({'error': 'Formato de token inválido'}), 401
        
        if not token:
            return jsonify({'error': 'Token no proporcionado'}), 401
        
        # Decodificar token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        # Verificar que el usuario existe y está activo
        user = user_repo.get_by_id(payload['user_id'])
        if not user or not user.is_active:
            return jsonify({'error': 'Usuario no válido'}), 401
        
        return f(payload, *args, **kwargs)
    
    return decorated


def admin_required(f):
    """
    Decorador para requerir rol de administrador.
    Debe usarse junto con @token_required.
    """
    @wraps(f)
    def decorated(payload, *args, **kwargs):
        if payload.get('role') != UserRole.ADMIN.value:
            return jsonify({'error': 'Acceso denegado. Se requiere rol de administrador'}), 403
        
        return f(payload, *args, **kwargs)
    
    return decorated


def get_user_by_id(user_id):
    """Obtiene un usuario por ID."""
    return user_repo.get_by_id(user_id)


def get_all_users():
    """Obtiene todos los usuarios."""
    return user_repo.get_all()


def change_user_role(user_id, new_role):
    """
    Cambia el rol de un usuario.
    
    Args:
        user_id: ID del usuario
        new_role: Nuevo rol (UserRole)
        
    Returns:
        tuple: (usuario_actualizado, mensaje_error)
    """
    # Verificar que haya al menos un admin
    if new_role == UserRole.USER:
        user = user_repo.get_by_id(user_id)
        if user and user.role == UserRole.ADMIN:
            if user_repo.count_admins() <= 1:
                return None, "No se puede remover el último administrador del sistema"
    
    updated_user = user_repo.update(user_id, {'role': new_role})
    return updated_user, None
