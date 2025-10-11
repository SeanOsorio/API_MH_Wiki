from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import (
    register_user, login_user, refresh_access_token,
    revoke_refresh_token, revoke_all_user_tokens, get_user_by_id
)
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
    Endpoint para registro de usuarios
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validaciones
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
        result = register_user(email, password)
        
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
    Endpoint para login de usuarios
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validaciones básicas
        if not email or not password:
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Formato de email inválido'}), 400
        
        # Autenticar usuario
        result = login_user(email, password)
        
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
    Endpoint para obtener información del usuario autenticado
    """
    try:
        user_id = get_jwt_identity()
        user = get_user_by_id(user_id)
        
        if user:
            return jsonify({
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "created_at": user.created_at.isoformat(),
                    "is_active": user.is_active
                }
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