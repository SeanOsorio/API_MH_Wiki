from flask import Blueprint, request, jsonify
from services.auth_service import register_user
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