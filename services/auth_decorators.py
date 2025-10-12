# -*- coding: utf-8 -*-
"""
🛡️ DECORADORES DE AUTORIZACIÓN
=============================
Decoradores para verificar roles y permisos en endpoints
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.auth_service import get_user_by_id, user_has_permission, user_has_role

def require_role(*allowed_roles):
    """
    Decorador que requiere que el usuario tenga uno de los roles especificados
    
    Usage:
        @require_role('admin', 'moderator')
        def some_endpoint():
            pass
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            
            # Verificar si el usuario tiene alguno de los roles permitidos
            user_role = claims.get('role', 'user')
            
            if user_role not in allowed_roles:
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': f'Se requiere uno de los siguientes roles: {", ".join(allowed_roles)}',
                    'required_roles': list(allowed_roles),
                    'user_role': user_role
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_permission(*required_permissions):
    """
    Decorador que requiere que el usuario tenga uno de los permisos especificados
    
    Usage:
        @require_permission('weapon_create', 'admin')
        def create_weapon():
            pass
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            
            # Obtener permisos del usuario desde el token
            user_permissions = claims.get('permissions', [])
            
            # Los admins tienen acceso a todo
            if 'admin' in user_permissions:
                return f(*args, **kwargs)
            
            # Verificar si el usuario tiene alguno de los permisos requeridos
            has_permission = any(perm in user_permissions for perm in required_permissions)
            
            if not has_permission:
                return jsonify({
                    'error': 'Permiso insuficiente',
                    'message': f'Se requiere uno de los siguientes permisos: {", ".join(required_permissions)}',
                    'required_permissions': list(required_permissions),
                    'user_permissions': user_permissions
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin():
    """
    Decorador que requiere rol de administrador
    
    Usage:
        @require_admin()
        def admin_only_endpoint():
            pass
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role', 'user')
            user_permissions = claims.get('permissions', [])
            
            if user_role != 'admin' and 'admin' not in user_permissions:
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'Solo los administradores pueden acceder a este endpoint',
                    'required_role': 'admin',
                    'user_role': user_role
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_own_resource_or_admin():
    """
    Decorador que permite acceso solo si es el propio recurso del usuario o es admin
    Útil para endpoints como /users/{user_id} donde un usuario solo puede ver sus datos
    
    Usage:
        @require_own_resource_or_admin()
        def get_user_profile(user_id):
            pass
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role', 'user')
            user_permissions = claims.get('permissions', [])
            
            # Obtener user_id del endpoint (puede venir de URL params o kwargs)
            resource_user_id = kwargs.get('user_id') or args[0] if args else None
            
            # Los admins pueden acceder a cualquier recurso
            if user_role == 'admin' or 'admin' in user_permissions:
                return f(*args, **kwargs)
            
            # Los usuarios solo pueden acceder a sus propios recursos
            if str(current_user_id) != str(resource_user_id):
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'Solo puedes acceder a tus propios datos',
                    'resource_user_id': resource_user_id,
                    'current_user_id': current_user_id
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def optional_auth():
    """
    Decorador que hace la autenticación opcional
    Si hay token válido, agrega la info del usuario
    Si no hay token, continúa sin autenticación
    
    Usage:
        @optional_auth()
        def public_endpoint():
            current_user_id = get_jwt_identity() if hasattr(g, 'jwt_identity') else None
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Intentar obtener JWT, pero no fallar si no existe
                from flask_jwt_extended import verify_jwt_in_request
                verify_jwt_in_request(optional=True)
            except:
                # Si no hay JWT válido o hay error, continuar sin autenticación
                pass
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ==========================================
# 🎯 FUNCIONES AUXILIARES
# ==========================================

def get_current_user_info():
    """
    Obtiene información completa del usuario actual desde el JWT
    """
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        return {
            'user_id': current_user_id,
            'role': claims.get('role', 'user'),
            'permissions': claims.get('permissions', [])
        }
    except:
        return None

def check_user_permission(permission):
    """
    Verifica si el usuario actual tiene un permiso específico
    """
    try:
        claims = get_jwt()
        user_permissions = claims.get('permissions', [])
        return permission in user_permissions or 'admin' in user_permissions
    except:
        return False

def is_current_user_admin():
    """
    Verifica si el usuario actual es administrador
    """
    try:
        claims = get_jwt()
        user_role = claims.get('role', 'user')
        user_permissions = claims.get('permissions', [])
        return user_role == 'admin' or 'admin' in user_permissions
    except:
        return False