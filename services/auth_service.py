import secrets
from typing import Dict, Any
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from config.database import get_db
from models.weapons_model import User, RefreshToken
from datetime import timedelta, datetime

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
    Autentica un usuario y genera tokens JWT (access y refresh)
    """
    db = next(get_db())
    try:
        # Buscar usuario por email
        user = db.query(User).filter(User.email == email, User.is_active == True).first()
        
        if not user or not verify_password(password, user.password_hash):
            return {'success': False, 'message': 'Credenciales inválidas'}
        
        # Crear tokens JWT
        access_token = create_access_token(
            identity=user.id,
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
                'email': user.email
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