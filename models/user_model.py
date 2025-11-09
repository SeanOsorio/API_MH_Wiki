"""
Modelo de Usuario para autenticación y autorización.
Incluye roles (admin/user) y gestión de contraseñas hasheadas.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from models.weapons_model import Base
import enum


class UserRole(enum.Enum):
    """Roles de usuario en el sistema."""
    USER = "user"  # Minúscula para coincidir con PostgreSQL enum
    ADMIN = "admin"  # Minúscula para coincidir con PostgreSQL enum


class User(Base):
    """
    Modelo de usuario para el sistema de autenticación.
    
    Atributos:
        id: Identificador único
        username: Nombre de usuario único
        email: Correo electrónico único
        password_hash: Contraseña hasheada con bcrypt
        role: Rol del usuario (USER o ADMIN)
        is_active: Estado de la cuenta
        created_at: Fecha de creación
        last_login: Última fecha de inicio de sesión
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]), 
                  nullable=False, default=UserRole.USER)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def to_json(self, include_sensitive=False):
        """
        Convierte el usuario a formato JSON.
        
        Args:
            include_sensitive: Si es True, incluye datos sensibles (solo para admin)
            
        Returns:
            dict: Representación JSON del usuario
        """
        data = {
            'id': self.id,
            'username': self.username,
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_sensitive:
            data['email'] = self.email
            data['last_login'] = self.last_login.isoformat() if self.last_login else None
            
        return data
    
    def __repr__(self):
        return f"<User {self.username} ({self.role.value})>"
