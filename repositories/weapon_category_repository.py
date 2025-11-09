"""
Repository para gestionar categorías de armas en PostgreSQL

Este módulo proporciona una capa de abstracción entre la lógica de negocio
y la base de datos PostgreSQL para operaciones CRUD de categorías de armas.
"""

from config.database import get_db
from models.weapons_model import WeaponCategory

class WeaponCategoryRepository:
    """
    Repository para operaciones CRUD de categorías de armas en PostgreSQL
    
    Proporciona métodos para:
    - Crear nuevas categorías
    - Obtener categorías (todas o por ID)
    - Actualizar categorías existentes
    - Eliminar categorías
    - Validar existencia de categorías
    """
    
    def get_all(self):
        """
        Obtener todas las categorías de armas
        
        Returns:
            list[WeaponCategory]: Lista de objetos WeaponCategory
        """
        db = next(get_db())
        try:
            categories = db.query(WeaponCategory).all()
            return categories
        finally:
            db.close()
    
    def get_by_id(self, category_id):
        """
        Obtener una categoría específica por su ID
        
        Args:
            category_id (int): ID de la categoría
            
        Returns:
            WeaponCategory|None: Objeto WeaponCategory si existe, None si no se encuentra
        """
        db = next(get_db())
        try:
            category = db.query(WeaponCategory).filter(WeaponCategory.id == category_id).first()
            return category
        finally:
            db.close()
    
    def create(self, data):
        """
        Crear una nueva categoría de arma
        
        Args:
            data (dict): Diccionario con los datos de la categoría
                - name (str): Nombre de la categoría (requerido)
                - description (str): Descripción de la categoría (opcional)
            
        Returns:
            WeaponCategory: Objeto de la categoría creada con su ID asignado
        """
        db = next(get_db())
        try:
            category = WeaponCategory(
                name=data['name'],
                description=data.get('description', '')
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            return category
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def update(self, category_id, data):
        """
        Actualizar una categoría existente
        
        Args:
            category_id (int): ID de la categoría a actualizar
            data (dict): Diccionario con los nuevos datos
                - name (str): Nuevo nombre de la categoría
                - description (str): Nueva descripción
            
        Returns:
            WeaponCategory|None: Objeto actualizado si existe, None si no se encuentra
        """
        db = next(get_db())
        try:
            category = db.query(WeaponCategory).filter(WeaponCategory.id == category_id).first()
            if category:
                category.name = data['name']
                category.description = data.get('description', '')
                db.commit()
                db.refresh(category)
            return category
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def delete(self, category_id):
        """
        Eliminar una categoría
        
        Args:
            category_id (int): ID de la categoría a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
        """
        db = next(get_db())
        try:
            category = db.query(WeaponCategory).filter(WeaponCategory.id == category_id).first()
            if category:
                db.delete(category)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def exists_by_name(self, name):
        """
        Verificar si existe una categoría con el nombre especificado
        
        Útil para validar duplicados antes de crear o actualizar
        
        Args:
            name (str): Nombre de la categoría a verificar
            
        Returns:
            bool: True si existe una categoría con ese nombre, False si no
        """
        db = next(get_db())
        try:
            exists = db.query(WeaponCategory).filter(WeaponCategory.name == name).first() is not None
            return exists
        finally:
            db.close()
