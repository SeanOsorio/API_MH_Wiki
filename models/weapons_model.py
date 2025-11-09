from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WeaponCategory(Base):
    __tablename__ = 'weapon_categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    icon_path = Column(String(255), nullable=True)  # Ruta a la imagen del icono (fallback)
    icon_data = Column(LargeBinary, nullable=True)  # Imagen almacenada como BYTEA
    icon_mime_type = Column(String(50), nullable=True)  # Tipo MIME (image/png, image/jpeg)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon_path': self.icon_path,
            'has_icon_data': self.icon_data is not None
        }

class Weapon(Base):
    __tablename__ = 'weapons'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('weapon_categories.id'))
    description = Column(String(255), nullable=True)
    image_path = Column(String(255), nullable=True)  # Ruta a la imagen del arma (fallback)
    image_data = Column(LargeBinary, nullable=True)  # Imagen almacenada como BYTEA
    image_mime_type = Column(String(50), nullable=True)  # Tipo MIME (image/png, image/jpeg)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'description': self.description,
            'image_path': self.image_path,
            'has_image_data': self.image_data is not None
        }
