from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import (
    register_user, login_user, refresh_access_token,
    revoke_refresh_token, revoke_all_user_tokens, get_user_by_id,
    get_user_with_role, update_user_role, get_all_users,
    get_all_roles, create_role, initialize_default_roles, create_admin_user
)
from services.auth_decorators import require_admin, require_role, require_permission, require_own_resource_or_admin
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def validate_email(email: str) -> bool:
    """
    Valida formato de email
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> dict:
    """
    Valida fortaleza de contraseña
    """
    if len(password) < 8:
        return {'valid': False, 'message': 'La contraseña debe tener al menos 8 caracteres'}
    
    if not re.search(r'[A-Z]', password):
        return {'valid': False, 'message': 'La contraseña debe contener al menos una letra mayúscula'}
    
    if not re.search(r'[a-z]', password):
        return {'valid': False, 'message': 'La contraseña debe contener al menos una letra minúscula'}
    
    if not re.search(r'\d', password):
        return {'valid': False, 'message': 'La contraseña debe contener al menos un número'}
    
    return {'valid': True}

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint para registro de usuarios con rol
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        role = data.get('role', 'user')  # Rol por defecto: user
        
        # Validaciones
        if not username:
            return jsonify({'error': 'El username es requerido'}), 400
            
        if not email:
            return jsonify({'error': 'El email es requerido'}), 400
        
        if not password:
            return jsonify({'error': 'La contraseña es requerida'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Formato de email inválido'}), 400
        
        password_validation = validate_password(password)
        if not password_validation['valid']:
            return jsonify({'error': password_validation['message']}), 400
        
        # Registrar usuario
        result = register_user(username, email, password, role)
        
        if result['success']:
            return jsonify({
                'message': 'Usuario registrado exitosamente',
                'user': result['user']
            }), 201
        else:
            return jsonify({'error': result['message']}), 400
    
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para login de usuarios (username o email)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validaciones básicas
        if not username or not password:
            return jsonify({'error': 'Username/email y contraseña son requeridos'}), 400
        
        # Autenticar usuario
        result = login_user(username, password)
        
        if result['success']:
            return jsonify({
                'message': 'Login exitoso',
                'access_token': result['access_token'],
                'refresh_token': result['refresh_token'],
                'expires_in': result['expires_in'],
                'refresh_expires_in': result['refresh_expires_in'],
                'user': result['user']
            }), 200
        else:
            return jsonify({'error': result['message']}), 401
    
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Endpoint para refrescar access token usando refresh token
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'error': 'Refresh token es requerido'}), 400
        
        # Refrescar token
        result = refresh_access_token(refresh_token)
        
        if result['success']:
            return jsonify({
                'message': 'Token refrescado exitosamente',
                'access_token': result['access_token'],
                'expires_in': result['expires_in']
            }), 200
        else:
            return jsonify({'error': result['message']}), 401
    
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Endpoint para logout (cierre de sesión) con revocación de tokens
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        refresh_token = data.get("refresh_token") if data else None
        
        if refresh_token:
            # Revocar refresh token específico
            result = revoke_refresh_token(refresh_token)
            
            if result["success"]:
                return jsonify({"message": result["message"]}), 200
            else:
                return jsonify({"error": result["message"]}), 400
        else:
            # Revocar todos los tokens del usuario (logout completo)
            result = revoke_all_user_tokens(user_id)
            
            if result["success"]:
                return jsonify({"message": "Sesión cerrada exitosamente (todos los dispositivos)"}), 200
            else:
                return jsonify({"error": result["message"]}), 400
    
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    Endpoint para obtener información completa del usuario autenticado (con rol)
    """
    try:
        user_id = get_jwt_identity()
        user_data = get_user_with_role(user_id)
        
        if user_data:
            return jsonify({
                "user": user_data
            }), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@auth_bp.route("/revoke-all", methods=["POST"])
@jwt_required()
def revoke_all_tokens():
    """
    Endpoint para revocar todos los refresh tokens del usuario
    """
    try:
        user_id = get_jwt_identity()
        
        result = revoke_all_user_tokens(user_id)
        
        if result["success"]:
            return jsonify({"message": "Todos los tokens han sido revocados exitosamente"}), 200
        else:
            return jsonify({"error": result["message"]}), 400
    
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# ==========================================
# 🛡️ ENDPOINTS DE GESTIÓN DE ROLES
# ==========================================

@auth_bp.route("/roles", methods=["GET"])
@jwt_required()
@require_permission('admin', 'role_management')
def get_roles():
    """
    Endpoint para obtener todos los roles disponibles (solo admins)
    """
    try:
        roles = get_all_roles()
        return jsonify({
            "message": "Roles obtenidos exitosamente",
            "roles": roles,
            "total": len(roles)
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@auth_bp.route("/roles", methods=["POST"])
@jwt_required()
@require_admin()
def create_new_role():
    """
    Endpoint para crear un nuevo rol (solo administradores)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        name = data.get('name', '').strip()
        description = data.get('description', '')
        permissions = data.get('permissions', [])
        
        if not name:
            return jsonify({'error': 'El nombre del rol es requerido'}), 400
        
        if not isinstance(permissions, list):
            return jsonify({'error': 'Los permisos deben ser una lista'}), 400
        
        role, message = create_role(name, description, permissions)
        
        if role:
            return jsonify({
                'message': message,
                'role': {
                    'id': role.id,
                    'name': role.name,
                    'description': role.description,
                    'permissions': permissions
                }
            }), 201
        else:
            return jsonify({'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

# ==========================================
# 👥 ENDPOINTS DE GESTIÓN DE USUARIOS
# ==========================================

@auth_bp.route("/users", methods=["GET"])
@jwt_required()
@require_permission('admin', 'user_management')
def get_all_users_endpoint():
    """
    Endpoint para obtener todos los usuarios (solo admins y moderadores)
    """
    try:
        users = get_all_users()
        return jsonify({
            "message": "Usuarios obtenidos exitosamente",
            "users": users,
            "total": len(users)
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@auth_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
@require_own_resource_or_admin()
def get_user_profile(user_id):
    """
    Endpoint para obtener perfil de usuario específico
    Los usuarios pueden ver su propio perfil, los admins pueden ver cualquiera
    """
    try:
        user_data = get_user_with_role(user_id)
        
        if user_data:
            return jsonify({
                "message": "Perfil obtenido exitosamente",
                "user": user_data
            }), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@auth_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@jwt_required()
@require_admin()
def change_user_role(user_id):
    """
    Endpoint para cambiar el rol de un usuario (solo administradores)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        new_role = data.get('role', '').strip()
        
        if not new_role:
            return jsonify({'error': 'El nuevo rol es requerido'}), 400
        
        user, message = update_user_role(user_id, new_role)
        
        if user:
            return jsonify({
                'message': message,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'new_role': new_role
                }
            }), 200
        else:
            return jsonify({'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

# ==========================================
# 🏗️ ENDPOINT DE INICIALIZACIÓN
# ==========================================

@auth_bp.route("/init", methods=["POST"])
def initialize_system():
    """
    Endpoint para inicializar el sistema con roles y usuario admin por defecto
    ⚠️ Solo debe usarse en desarrollo o primera instalación
    """
    try:
        # Crear roles por defecto
        created_roles = initialize_default_roles()
        
        # Crear usuario admin por defecto
        admin_user = create_admin_user()
        
        return jsonify({
            'message': 'Sistema inicializado exitosamente',
            'created_roles': created_roles,
            'admin_created': admin_user is not None,
            'admin_credentials': {
                'username': 'admin',
                'password': 'admin123',
                'note': '⚠️ Cambia esta contraseña inmediatamente'
            } if admin_user else None
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error al inicializar sistema: {str(e)}'}), 500