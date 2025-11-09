"""
Repositorio para operaciones de base de datos de usuarios.
"""

from config.database import get_db
from models.user_model import User, UserRole
from sqlalchemy import or_
from datetime import datetime


class UserRepository:
    """Repositorio para gestionar usuarios en la base de datos."""
    
    def get_all(self):
        """Obtiene todos los usuarios."""
        db = next(get_db())
        try:
            return db.query(User).all()
        finally:
            db.close()
    
    def get_by_id(self, user_id):
        """
        Busca un usuario por su ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            User o None si no existe
        """
        db = next(get_db())
        try:
            return db.query(User).filter_by(id=user_id).first()
        finally:
            db.close()
    
    def create(self, data):
        """
        Crea un nuevo usuario.
        
        Args:
            data: Diccionario con los datos del usuario
            
        Returns:
            User: Usuario creado
        """
        db = next(get_db())
        try:
            user = User(**data)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        finally:
            db.close()
    
    def update(self, user_id, data):
        """
        Actualiza un usuario existente.
        
        Args:
            user_id: ID del usuario
            data: Diccionario con los datos a actualizar
            
        Returns:
            User o None si no existe
        """
        db = next(get_db())
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                db.commit()
                db.refresh(user)
            return user
        finally:
            db.close()
    
    def delete(self, user_id):
        """
        Elimina un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si se eliminó, False si no
        """
        db = next(get_db())
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if user:
                db.delete(user)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def get_by_username(self, username):
        """
        Busca un usuario por su nombre de usuario.
        
        Args:
            username: Nombre de usuario a buscar
            
        Returns:
            User o None si no existe
        """
        db = next(get_db())
        try:
            return db.query(User).filter_by(username=username).first()
        finally:
            db.close()
    
    def get_by_email(self, email):
        """
        Busca un usuario por su email.
        
        Args:
            email: Email a buscar
            
        Returns:
            User o None si no existe
        """
        db = next(get_db())
        try:
            return db.query(User).filter_by(email=email).first()
        finally:
            db.close()
    
    def exists_by_username_or_email(self, username, email):
        """
        Verifica si existe un usuario con el username o email dado.
        
        Args:
            username: Nombre de usuario
            email: Email
            
        Returns:
            bool: True si existe, False si no
        """
        db = next(get_db())
        try:
            return db.query(User).filter(
                or_(User.username == username, User.email == email)
            ).first() is not None
        finally:
            db.close()
    
    def update_last_login(self, user_id):
        """
        Actualiza la fecha de último login del usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si se actualizó correctamente
        """
        db = next(get_db())
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if user:
                user.last_login = datetime.utcnow()
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def get_all_admins(self):
        """
        Obtiene todos los usuarios con rol de administrador.
        
        Returns:
            list: Lista de usuarios admin
        """
        db = next(get_db())
        try:
            return db.query(User).filter(User.role == UserRole.ADMIN).all()
        finally:
            db.close()
    
    def count_admins(self):
        """
        Cuenta cuántos administradores hay en el sistema.
        
        Returns:
            int: Número de administradores
        """
        db = next(get_db())
        try:
            return db.query(User).filter(User.role == UserRole.ADMIN).count()
        finally:
            db.close()
    
    def deactivate_user(self, user_id):
        """
        Desactiva un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si se desactivó correctamente
        """
        db = next(get_db())
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if user:
                user.is_active = False
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def activate_user(self, user_id):
        """
        Activa un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si se activó correctamente
        """
        db = next(get_db())
        try:
            user = db.query(User).filter_by(id=user_id).first()
            if user:
                user.is_active = True
                db.commit()
                return True
            return False
        finally:
            db.close()
