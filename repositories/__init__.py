"""
Módulo de repositories para acceso a datos en MongoDB
"""

from .weapon_category_repository import WeaponCategoryRepository
from .weapon_repository import WeaponRepository

__all__ = ['WeaponCategoryRepository', 'WeaponRepository']
