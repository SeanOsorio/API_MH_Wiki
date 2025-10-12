
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.weapons_service import (
	get_all_categories, get_category_by_id, create_category, update_category, delete_category,
	get_weapon_by_id, create_weapon, update_weapon, delete_weapon
)
from services.auth_decorators import require_permission, require_role

weapons_bp = Blueprint('weapons', __name__)

# --- Endpoints para categorías ---
# Obtener todas las categorías (requiere autenticación)
@weapons_bp.route('/categories', methods=['GET'])
@jwt_required()
@require_permission('category_read')
def list_categories():
	categories = get_all_categories()
	return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in categories])

# Obtener una categoría por ID (requiere lectura de categorías)
@weapons_bp.route('/categories/<int:category_id>', methods=['GET'])
@jwt_required()
@require_permission('category_read')
def get_category(category_id):
	category = get_category_by_id(category_id)
	if category:
		return jsonify({'id': category.id, 'name': category.name, 'description': category.description})
	return jsonify({'error': 'Categoría no encontrada'}), 404

# Crear una nueva categoría (requiere permisos de creación)
@weapons_bp.route('/categories', methods=['POST'])
@jwt_required()
@require_permission('category_create')
def create_new_category():
	data = request.json
	
	if not data or not data.get('name'):
		return jsonify({'error': 'El nombre de la categoría es requerido'}), 400
	
	try:
		category = create_category(data)
		return jsonify({
			'message': 'Categoría creada exitosamente',
			'category': {
				'id': category.id, 
				'name': category.name, 
				'description': category.description
			}
		}), 201
	except Exception as e:
		return jsonify({'error': f'Error al crear categoría: {str(e)}'}), 500

# Actualizar una categoría (requiere permisos de actualización)
@weapons_bp.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
@require_permission('category_update')
def update_category_endpoint(category_id):
	data = request.json
	
	if not data:
		return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
	
	try:
		category = update_category(category_id, data)
		if category:
			return jsonify({
				'message': 'Categoría actualizada exitosamente',
				'category': {
					'id': category.id, 
					'name': category.name, 
					'description': category.description
				}
			})
		return jsonify({'error': 'Categoría no encontrada'}), 404
	except Exception as e:
		return jsonify({'error': f'Error al actualizar categoría: {str(e)}'}), 500

# Eliminar una categoría (requiere permisos de eliminación)
@weapons_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
@require_permission('category_delete')
def delete_category_endpoint(category_id):
	try:
		category = delete_category(category_id)
		if category:
			return jsonify({
				'message': f'Categoría "{category.name}" eliminada exitosamente'
			})
		return jsonify({'error': 'Categoría no encontrada'}), 404
	except Exception as e:
		return jsonify({'error': f'Error al eliminar categoría: {str(e)}'}), 500

# --- Endpoints para armas ---

# Obtener todas las armas (requiere lectura de armas)
@weapons_bp.route('/weapons', methods=['GET'])
@jwt_required()
@require_permission('weapon_read')
def list_weapons():
	try:
		from config.database import get_db
		from models.weapons_model import Weapon
		
		db = next(get_db())
		weapons = db.query(Weapon).all()
		
		return jsonify([{
			'id': w.id, 
			'name': w.name, 
			'category_id': w.category_id, 
			'description': w.description
		} for w in weapons])
	except Exception as e:
		return jsonify({'error': f'Error al obtener armas: {str(e)}'}), 500

# Obtener un arma por ID (requiere lectura de armas)
@weapons_bp.route('/weapons/<int:weapon_id>', methods=['GET'])
@jwt_required()
@require_permission('weapon_read')
def get_weapon(weapon_id):
	weapon = get_weapon_by_id(weapon_id)
	if weapon:
		return jsonify({
			'id': weapon.id, 
			'name': weapon.name, 
			'category_id': weapon.category_id, 
			'description': weapon.description
		})
	return jsonify({'error': 'Arma no encontrada'}), 404

# Crear una nueva arma (requiere permisos de creación)
@weapons_bp.route('/weapons', methods=['POST'])
@jwt_required()
@require_permission('weapon_create')
def create_new_weapon():
	data = request.json
	
	if not data or not data.get('name'):
		return jsonify({'error': 'El nombre del arma es requerido'}), 400
	
	try:
		weapon = create_weapon(data)
		return jsonify({
			'message': 'Arma creada exitosamente',
			'weapon': {
				'id': weapon.id, 
				'name': weapon.name, 
				'category_id': weapon.category_id, 
				'description': weapon.description
			}
		}), 201
	except Exception as e:
		return jsonify({'error': f'Error al crear arma: {str(e)}'}), 500

# Actualizar un arma (requiere permisos de actualización)
@weapons_bp.route('/weapons/<int:weapon_id>', methods=['PUT'])
@jwt_required()
@require_permission('weapon_update')
def update_weapon_endpoint(weapon_id):
	data = request.json
	
	if not data:
		return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
	
	try:
		weapon = update_weapon(weapon_id, data)
		if weapon:
			return jsonify({
				'message': 'Arma actualizada exitosamente',
				'weapon': {
					'id': weapon.id, 
					'name': weapon.name, 
					'category_id': weapon.category_id, 
					'description': weapon.description
				}
			})
		return jsonify({'error': 'Arma no encontrada'}), 404
	except Exception as e:
		return jsonify({'error': f'Error al actualizar arma: {str(e)}'}), 500

# Eliminar un arma (requiere permisos de eliminación)
@weapons_bp.route('/weapons/<int:weapon_id>', methods=['DELETE'])
@jwt_required()
@require_permission('weapon_delete')
def delete_weapon_endpoint(weapon_id):
	try:
		weapon = delete_weapon(weapon_id)
		if weapon:
			return jsonify({
				'message': f'Arma "{weapon.name}" eliminada exitosamente'
			})
		return jsonify({'error': 'Arma no encontrada'}), 404
	except Exception as e:
		return jsonify({'error': f'Error al eliminar arma: {str(e)}'}), 500
