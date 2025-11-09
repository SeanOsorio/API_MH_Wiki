"""
Controlador REST para autenticación y gestión de usuarios.

Endpoints:
- POST /auth/register - Registrar nuevo usuario
- POST /auth/login - Iniciar sesión
- GET  /auth/me - Obtener perfil del usuario actual
- GET  /auth/users - Listar usuarios (solo admin)
- PUT  /auth/users/{id}/role - Cambiar rol de usuario (solo admin)
- GET  /auth/source - Ver código fuente (requiere admin)
"""

from flask import Blueprint, request, jsonify, send_file
from services import auth_service
# from services import captcha_service  # Ya no se usa, ahora usamos Google reCAPTCHA
from models.user_model import UserRole
import os

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra un nuevo usuario en el sistema.
    
    Body JSON:
        {
            "username": "string (min 3 caracteres)",
            "email": "string (email válido)",
            "password": "string (min 6 caracteres)"
        }
        
    Returns:
        201: Usuario creado exitosamente
        400: Datos inválidos
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Registrar usuario (siempre como USER, los admins se crean manualmente)
    user, error = auth_service.register_user(username, email, password, UserRole.USER)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'user': user.to_json()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autentica a un usuario y devuelve un token JWT.
    
    Body JSON:
        {
            "username": "string (username o email)",
            "password": "string"
        }
        
    Returns:
        200: Login exitoso con token
        401: Credenciales inválidas
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username y password son requeridos'}), 400
    
    token, user, error = auth_service.login_user(username, password)
    
    if error:
        return jsonify({'error': error}), 401
    
    return jsonify({
        'message': 'Login exitoso',
        'token': token,
        'user': user.to_json(include_sensitive=True)
    }), 200


@auth_bp.route('/me', methods=['GET'])
@auth_service.token_required
def get_profile(payload):
    """
    Obtiene el perfil del usuario actual.
    
    Headers:
        Authorization: Bearer <token>
        
    Returns:
        200: Perfil del usuario
        401: Token inválido
    """
    user = auth_service.get_user_by_id(payload['user_id'])
    
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({
        'user': user.to_json(include_sensitive=True)
    }), 200


@auth_bp.route('/users', methods=['GET'])
@auth_service.token_required
@auth_service.admin_required
def list_users(payload):
    """
    Lista todos los usuarios del sistema (solo admin).
    
    Headers:
        Authorization: Bearer <token>
        
    Returns:
        200: Lista de usuarios
        403: No es administrador
    """
    users = auth_service.get_all_users()
    
    return jsonify({
        'users': [user.to_json(include_sensitive=True) for user in users],
        'total': len(users)
    }), 200


@auth_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@auth_service.token_required
@auth_service.admin_required
def change_role(payload, user_id):
    """
    Cambia el rol de un usuario (solo admin).
    
    Headers:
        Authorization: Bearer <token>
        
    Body JSON:
        {
            "role": "admin" | "user"
        }
        
    Returns:
        200: Rol actualizado
        400: Datos inválidos
        403: No es administrador
    """
    data = request.get_json()
    
    if not data or 'role' not in data:
        return jsonify({'error': 'El campo role es requerido'}), 400
    
    role_str = data['role'].lower()
    
    try:
        if role_str == 'admin':
            new_role = UserRole.ADMIN
        elif role_str == 'user':
            new_role = UserRole.USER
        else:
            return jsonify({'error': 'Rol inválido. Use "admin" o "user"'}), 400
        
        user, error = auth_service.change_user_role(user_id, new_role)
        
        if error:
            return jsonify({'error': error}), 400
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'message': f'Rol actualizado a {new_role.value}',
            'user': user.to_json(include_sensitive=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Las siguientes funciones están deshabilitadas porque ahora usamos Google reCAPTCHA en el frontend
# Si necesitas reactivarlas, descomenta y reinstala captcha_service.py

# @auth_bp.route('/captcha', methods=['POST'])
# def generate_captcha():
#     """
#     Genera una nueva imagen de CAPTCHA.
#     
#     Returns:
#         200: Imagen CAPTCHA y ID
#     """
#     captcha_id, image_bytes, _ = captcha_service.create_captcha()
#     
#     # Enviar imagen
#     return send_file(
#         image_bytes,
#         mimetype='image/png',
#         as_attachment=False,
#         download_name='captcha.png',
#         headers={'X-Captcha-ID': captcha_id}
#     )


# @auth_bp.route('/captcha/verify', methods=['POST'])
# def verify_captcha():
#     """
#     Verifica un CAPTCHA ingresado por el usuario.
#     
#     Body JSON:
#         {
#             "captcha_id": "string",
#             "captcha_text": "string"
#         }
#         
#     Returns:
#         200: CAPTCHA válido
#         400: CAPTCHA inválido
#     """
#     data = request.get_json()
#     
#     if not data:
#         return jsonify({'error': 'No se proporcionaron datos'}), 400
#     
#     captcha_id = data.get('captcha_id')
#     captcha_text = data.get('captcha_text')
#     
#     if not captcha_id or not captcha_text:
#         return jsonify({'error': 'captcha_id y captcha_text son requeridos'}), 400
#     
#     is_valid, message = captcha_service.verify_captcha(captcha_id, captcha_text)
#     
#     if not is_valid:
#         return jsonify({'error': message}), 400
#     
#     return jsonify({'message': message}), 200


@auth_bp.route('/source', methods=['POST'])
@auth_service.token_required
@auth_service.admin_required
def view_source(payload):
    """
    Permite ver el código fuente (solo admin).
    Nota: El CAPTCHA ahora se verifica con Google reCAPTCHA en el frontend.
    
    Headers:
        Authorization: Bearer <token>
        
    Body JSON:
        {
            "file_path": "string (opcional)"
        }
        
    Returns:
        200: Contenido del archivo
        403: No es administrador
        404: Archivo no encontrado
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    
    # Nota: El CAPTCHA ahora se verifica con Google reCAPTCHA en el frontend
    # Ya no necesitamos verificar CAPTCHA en el backend
    
    # Obtener archivo solicitado
    file_path = data.get('file_path', 'app.py')
    
    # Validar que el archivo esté en el proyecto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(project_root, file_path)
    
    # Seguridad: evitar acceso fuera del proyecto
    if not os.path.abspath(full_path).startswith(project_root):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    if not os.path.exists(full_path):
        return jsonify({'error': 'Archivo no encontrado'}), 404
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'file_path': file_path,
            'content': content,
            'lines': len(content.split('\n')),
            'size_bytes': len(content.encode('utf-8'))
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error leyendo archivo: {str(e)}'}), 500


@auth_bp.route('/source/files', methods=['GET'])
@auth_service.token_required
@auth_service.admin_required
def list_source_files(payload):
    """
    Lista los archivos Python disponibles en el proyecto (solo admin).
    
    Headers:
        Authorization: Bearer <token>
        
    Returns:
        200: Lista de archivos
        403: No es administrador
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    python_files = []
    
    for root, dirs, files in os.walk(project_root):
        # Ignorar carpetas específicas
        dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', '.git', 'images']]
        
        for file in files:
            if file.endswith('.py'):
                rel_path = os.path.relpath(os.path.join(root, file), project_root)
                python_files.append(rel_path)
    
    return jsonify({
        'files': sorted(python_files),
        'total': len(python_files)
    }), 200
