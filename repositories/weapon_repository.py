"""
Repository para gestionar armas en PostgreSQL

Este módulo proporciona una capa de abstracción entre la lógica de negocio
y la base de datos PostgreSQL para operaciones CRUD de armas.
"""

from config.database import get_db
from models.weapons_model import Weapon

class WeaponRepository:
    """
    Repository para operaciones CRUD de armas en PostgreSQL
    
    Proporciona métodos para:
    - Crear nuevas armas
    - Obtener armas (todas, por ID, o por categoría)
    - Actualizar armas existentes
    - Eliminar armas
    - Contar armas por categoría
    """
    
    def get_all(self):
        """
        Obtener todas las armas
        
        Returns:
            list[Weapon]: Lista de objetos Weapon
        """
        db = next(get_db())
        try:
            weapons = db.query(Weapon).all()
            return weapons
        finally:
            db.close()
    
    def get_by_id(self, weapon_id):
        """
        Obtener un arma específica por su ID
        
        Args:
            weapon_id (int): ID del arma
            
        Returns:
            Weapon|None: Objeto Weapon si existe, None si no se encuentra
        """
        db = next(get_db())
        try:
            weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
            return weapon
        finally:
            db.close()
    
    def get_by_category(self, category_id):
        """
        Obtener todas las armas de una categoría específica
        
        Args:
            category_id (int): ID de la categoría
            
        Returns:
            list[Weapon]: Lista de armas que pertenecen a la categoría
        """
        db = next(get_db())
        try:
            weapons = db.query(Weapon).filter(Weapon.category_id == category_id).all()
            return weapons
        finally:
            db.close()
    
    def create(self, data):
        """
        Crear una nueva arma
        
        Args:
            data (dict): Diccionario con los datos del arma
                - name (str): Nombre del arma (requerido)
                - category_id (int): ID de la categoría (requerido)
                - description (str): Descripción del arma (opcional)
            
        Returns:
            Weapon: Objeto del arma creada con su ID asignado
        """
        db = next(get_db())
        try:
            weapon = Weapon(
                name=data['name'],
                category_id=data['category_id'],
                description=data.get('description', '')
            )
            db.add(weapon)
            db.commit()
            db.refresh(weapon)
            return weapon
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def update(self, weapon_id, data):
        """
        Actualizar un arma existente
        
        Args:
            weapon_id (int): ID del arma a actualizar
            data (dict): Diccionario con los nuevos datos
                - name (str): Nuevo nombre del arma
                - category_id (int): Nueva categoría
                - description (str): Nueva descripción
            
        Returns:
            Weapon|None: Objeto actualizado si existe, None si no se encuentra
        """
        db = next(get_db())
        try:
            weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
            if weapon:
                weapon.name = data['name']
                weapon.category_id = data['category_id']
                weapon.description = data.get('description', '')
                db.commit()
                db.refresh(weapon)
            return weapon
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def delete(self, weapon_id):
        """
        Eliminar un arma
        
        Args:
            weapon_id (int): ID del arma a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
        """
        db = next(get_db())
        try:
            weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
            if weapon:
                db.delete(weapon)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def count_by_category(self, category_id):
        """
        Contar cuántas armas pertenecen a una categoría específica
        
        Útil para validar si una categoría tiene armas antes de eliminarla
        
        Args:
            category_id (int): ID de la categoría
            
        Returns:
            int: Cantidad de armas en la categoría
        """
        db = next(get_db())
        try:
            count = db.query(Weapon).filter(Weapon.category_id == category_id).count()
            return count
        finally:
            db.close()
