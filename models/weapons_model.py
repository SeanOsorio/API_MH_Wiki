
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Modelo para roles
class Role(Base):
	__tablename__ = 'roles'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(50), nullable=False, unique=True)
	description = Column(String(255), nullable=True)
	permissions = Column(Text, nullable=True)  # JSON string con permisos
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
	
	# Relación con usuarios
	users = relationship("User", back_populates="role")

# Modelo para usuarios
class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String(80), nullable=False, unique=True, index=True)
	email = Column(String(120), nullable=False, unique=True, index=True)
	password_hash = Column(String(128), nullable=False)
	role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, default=2)  # Default: user role
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
	
	# Relaciones
	role = relationship("Role", back_populates="users")
	refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

# Modelo para refresh tokens
class RefreshToken(Base):
	__tablename__ = 'refresh_tokens'
	id = Column(Integer, primary_key=True, autoincrement=True)
	token = Column(Text, nullable=False, unique=True, index=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	expires_at = Column(DateTime, nullable=False)
	is_revoked = Column(Boolean, default=False, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
	
	# Relación con usuario
	user = relationship("User", back_populates="refresh_tokens")

# Modelo para categorías de armas
class WeaponCategory(Base):
	__tablename__ = 'weapon_categories'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(100), nullable=False, unique=True)
	description = Column(String(255), nullable=True)

# Modelo para armas
class Weapon(Base):
	__tablename__ = 'weapons'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(100), nullable=False)
	category_id = Column(Integer, ForeignKey('weapon_categories.id'))
	description = Column(String(255), nullable=True)
