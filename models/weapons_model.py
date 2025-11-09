from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WeaponCategory(Base):
    __tablename__ = 'weapon_categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Weapon(Base):
    __tablename__ = 'weapons'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('weapon_categories.id'))
    description = Column(String(255), nullable=True)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'description': self.description
        }
