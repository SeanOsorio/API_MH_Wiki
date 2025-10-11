from typing import Dict, Any
from flask_bcrypt import Bcrypt
from config.database import get_db
from models.weapons_model import User

bcrypt = Bcrypt()

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')

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