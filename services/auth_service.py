from typing import Dict, Any
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from config.database import get_db
from models.weapons_model import User
from datetime import timedelta

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

def register_user(email: str, password: str) -> Dict[str, Any]:
    """
    Registra un nuevo usuario
    """
    db = next(get_db())
    try:
        # Verificar si el email ya existe
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return {'success': False, 'message': 'El email ya está registrado'}
        
        # Crear nuevo usuario
        password_hash = hash_password(password)
        new_user = User(
            email=email,
            password_hash=password_hash
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            'success': True,
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'created_at': new_user.created_at.isoformat()
            }
        }
    
    except Exception as e:
        db.rollback()
        return {'success': False, 'message': f'Error al registrar usuario: {str(e)}'}
    
    finally:
        db.close()

def login_user(email: str, password: str) -> Dict[str, Any]:
    """
    Autentica un usuario y genera un token JWT
    """
    db = next(get_db())
    try:
        # Buscar usuario por email
        user = db.query(User).filter(User.email == email, User.is_active == True).first()
        
        if not user or not verify_password(password, user.password_hash):
            return {'success': False, 'message': 'Credenciales inválidas'}
        
        # Crear token JWT con expiración de 1 hora
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1)
        )
        
        return {
            'success': True,
            'access_token': access_token,
            'expires_in': 3600,  # 1 hora en segundos
            'user': {
                'id': user.id,
                'email': user.email
            }
        }
    
    except Exception as e:
        return {'success': False, 'message': f'Error en el login: {str(e)}'}
    
    finally:
        db.close()