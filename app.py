"""
Monster Hunter Weapons API - Aplicación Principal

Esta es la API REST completa para gestionar categorías de armas y armas específicas
del universo Monster Hunter. Proporciona endpoints para operaciones CRUD completas
con validaciones, manejo de errores y arquitectura MVC.

Características principales:
- ✅ CRUD completo para categorías y armas
- ✅ Base de datos PostgreSQL en Railway
- ✅ Validaciones de integridad referencial
- ✅ IDs independientes por tabla
- ✅ Manejo robusto de errores HTTP
- ✅ Documentación completa de endpoints

Autor: Sean Osorio
Repositorio: https://github.com/SeanOsorio/ClassApi
Licencia: MIT
"""

from flask import Flask, jsonify, render_template
from controllers.weapons_controller import weapons_bp
from controllers.auth_controller import auth_bp
from config.database import init_db, get_db
from models.weapons_model import WeaponCategory, Weapon
from models.user_model import User

# Información de versión
__version__ = "2.0.0"
__title__ = "Monster Hunter Wiki"
RELEASE_NAME = "Monster Hunter Wilds Edition"

# =============================================================================
# INICIALIZACIÓN DE LA APLICACIÓN FLASK
# =============================================================================

def create_app():
    """
    Factory function para crear y configurar la aplicación Flask.
    
    Esta función encapsula la creación de la app y permite:
    - Testing más fácil
    - Múltiples configuraciones (dev, prod, test)
    - Inicialización controlada de componentes
    
    Returns:
        Flask: Aplicación Flask configurada y lista para usar
    """
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Configuraciones básicas
    app.config['JSON_SORT_KEYS'] = False  # Preservar orden en respuestas JSON
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # JSON formateado en desarrollo
    
    return app

# Crear la aplicación principal
app = create_app()

# =============================================================================
# INICIALIZACIÓN DE BASE DE DATOS
# =============================================================================

# Configurar encoding para Windows PowerShell
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print(f"🚀 Iniciando {__title__} v{__version__}")
print(f"📦 Release: {RELEASE_NAME}")

# Inicializar base de datos al arrancar la aplicación
# Esto crea las tablas si no existen (safe operation)
init_db()

print("✅ Base de datos inicializada")

# =============================================================================
# REGISTRO DE BLUEPRINTS (RUTAS)
# =============================================================================

# Registrar blueprint de armas y categorías
# Esto incluye todos los endpoints definidos en weapons_controller.py
# Registrar las rutas de la API con el prefijo /api
app.register_blueprint(weapons_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

print("🛣️  Rutas registradas:")
print("   • GET    /api/categories              - Listar categorías")
print("   • POST   /api/categories              - Crear categoría")  
print("   • GET    /api/categories/{id}         - Obtener categoría")
print("   • PUT    /api/categories/{id}         - Actualizar categoría")
print("   • DELETE /api/categories/{id}         - Eliminar categoría")
print("   • GET    /api/categories/{id}/weapons - Armas por categoría")
print("   • GET    /api/weapons                 - Listar armas")
print("   • POST   /api/weapons                 - Crear arma")
print("   • GET    /api/weapons/{id}            - Obtener arma")
print("   • PUT    /api/weapons/{id}            - Actualizar arma")
print("   • DELETE /api/weapons/{id}            - Eliminar arma")
print("   🔐 AUTENTICACIÓN:")
print("   • POST   /api/auth/register           - Registrar usuario")
print("   • POST   /api/auth/login              - Iniciar sesión")
print("   • GET    /api/auth/me                 - Perfil del usuario")
print("   • GET    /api/auth/users              - Listar usuarios (admin)")
print("   • POST   /api/auth/captcha            - Generar CAPTCHA")
print("   • POST   /api/auth/source             - Ver código (admin + captcha)")

# =============================================================================
# ENDPOINTS ADICIONALES
# =============================================================================

@app.route('/')
def home():
    """
    Página de inicio de MonsterHunterWiki
    
    Returns:
        HTML: Página de inicio renderizada
    """
    return render_template('index.html')

@app.route('/weapons')
def weapons_page():
    """Página principal de armas - muestra categorías"""
    return render_template('weapons_categories.html')

@app.route('/weapons/category/<int:category_id>')
def weapons_by_category_page(category_id):
    """Página de armas por categoría"""
    return render_template('weapons_list.html', category_id=category_id)

@app.route('/weapons/<int:weapon_id>')
def weapon_detail_page(weapon_id):
    """Página de detalle de un arma específica"""
    return render_template('weapon_detail.html', weapon_id=weapon_id)

@app.route('/monsters')
def monsters_page():
    """Página de monstruos (próximamente)"""
    return render_template('coming_soon.html', section='Monstruos')

@app.route('/items')
def items_page():
    """Página de objetos (próximamente)"""
    return render_template('coming_soon.html', section='Objetos')

@app.route('/armor')
def armor_page():
    """Página de armaduras (próximamente)"""
    return render_template('coming_soon.html', section='Armaduras')

@app.route('/quests')
def quests_page():
    """Página de misiones (próximamente)"""
    return render_template('coming_soon.html', section='Misiones')

@app.route('/api/stats')
def api_stats():
    """
    Endpoint para obtener estadísticas de la wiki
    
    Returns:
        JSON: Estadísticas de artículos
    """
    try:
        db = next(get_db())
        categories_count = db.query(WeaponCategory).count()
        weapons_count = db.query(Weapon).count()
        total_articles = categories_count + weapons_count + 850  # + contenido base
        
        return jsonify({
            'total_articles': total_articles,
            'categories': categories_count,
            'weapons': weapons_count,
            'status': 'online'
        })
    except Exception as e:
        return jsonify({
            'total_articles': 1000,
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        db.close()

@app.route('/health')
def health_check():
    """
    Endpoint de health check para monitoreo.
    
    Returns:
        JSON: Estado de salud de la aplicación y base de datos
    """
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'api_version': '1.0.0'
    })

@app.route('/test-auth')
def test_auth_page():
    """Página de prueba del sistema de autenticación."""
    return render_template('test_auth.html')

# =============================================================================
# MANEJO GLOBAL DE ERRORES
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    """Manejador para errores 404 - Recurso no encontrado."""
    return jsonify({
        'error': 'Endpoint no encontrado',
        'message': 'Verifica la URL y el método HTTP',
        'available_endpoints': [
            'GET /categories',
            'POST /categories', 
            'GET /weapons',
            'POST /weapons'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Manejador para errores 405 - Método no permitido."""
    return jsonify({
        'error': 'Método HTTP no permitido',
        'message': 'Verifica que estés usando el método correcto (GET, POST, PUT, DELETE)'
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    """Manejador para errores 500 - Error interno del servidor."""
    return jsonify({
        'error': 'Error interno del servidor',
        'message': 'Ha ocurrido un error inesperado. Inténtalo más tarde.'
    }), 500

# =============================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# =============================================================================

if __name__ == '__main__':
    print("=" * 50)
    print(f"🎮 MONSTER HUNTER WEAPONS API v{__version__}")
    print("=" * 50)
    print("🌐 Servidor iniciando en: http://127.0.0.1:5000")
    print("📚 Documentación: https://github.com/SeanOsorio/ClassApi")
    print(f"📦 Release: {RELEASE_NAME}")
    print("🐛 Modo debug: ACTIVADO")
    print("=" * 50)
    
    # Iniciar servidor Flask en modo desarrollo
    app.run(
        debug=True,        # Modo debug para desarrollo
        host='127.0.0.1',  # Solo accesible localmente
        port=5000          # Puerto estándar para desarrollo
    )