from repositories.weapon_category_repository import WeaponCategoryRepository
from repositories.weapon_repository import WeaponRepository

category_repo = WeaponCategoryRepository()
weapon_repo = WeaponRepository()

def get_all_categories():
    categories = category_repo.get_all()
    return [cat.to_json() for cat in categories]

def get_category_by_id(category_id):
    category = category_repo.get_by_id(category_id)
    return category.to_json() if category else None

def create_category(data):
    if 'name' not in data or not data['name'].strip():
        raise ValueError("El campo 'name' es requerido")
    if category_repo.exists_by_name(data['name']):
        raise ValueError(f"Ya existe una categoría con el nombre '{data['name']}'")
    category = category_repo.create(data)
    return category.to_json()

def update_category(category_id, data):
    if 'name' not in data or not data['name'].strip():
        raise ValueError("El campo 'name' es requerido")
    category = category_repo.update(category_id, data)
    return category.to_json() if category else None

def delete_category(category_id):
    weapons_count = weapon_repo.count_by_category(category_id)
    if weapons_count > 0:
        raise ValueError(f"No se puede eliminar la categoría porque tiene {weapons_count} arma(s) asociada(s)")
    return category_repo.delete(category_id)

def get_all_weapons():
    weapons = weapon_repo.get_all()
    return [weapon.to_json() for weapon in weapons]

def get_weapon_by_id(weapon_id):
    weapon = weapon_repo.get_by_id(weapon_id)
    return weapon.to_json() if weapon else None

def get_weapons_by_category(category_id):
    weapons = weapon_repo.get_by_category(category_id)
    return [weapon.to_json() for weapon in weapons]

def create_weapon(data):
    if 'name' not in data or not data['name'].strip():
        raise ValueError("El campo 'name' es requerido")
    if 'category_id' not in data:
        raise ValueError("El campo 'category_id' es requerido")
    category = category_repo.get_by_id(data['category_id'])
    if not category:
        raise ValueError(f"La categoría con ID '{data['category_id']}' no existe")
    weapon = weapon_repo.create(data)
    return weapon.to_json()

def update_weapon(weapon_id, data):
    if 'name' not in data or not data['name'].strip():
        raise ValueError("El campo 'name' es requerido")
    if 'category_id' not in data:
        raise ValueError("El campo 'category_id' es requerido")
    category = category_repo.get_by_id(data['category_id'])
    if not category:
        raise ValueError(f"La categoría con ID '{data['category_id']}' no existe")
    weapon = weapon_repo.update(weapon_id, data)
    return weapon.to_json() if weapon else None

def delete_weapon(weapon_id):
    return weapon_repo.delete(weapon_id)
