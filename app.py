
#!/usr/bin/env python3
"""
🚀 Parcial1Web - Sistema de Autenticación API
==============================================

Ejecuta este archivo para iniciar la aplicación completa:
    python app.py

El sistema se auto-configura automáticamente al iniciar.
"""

import os
import sys
from pathlib import Path
from datetime import timedelta
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from controllers.weapons_controller import weapons_bp
from controllers.auth_controller import auth_bp


def setup_environment():
    """
    🔧 Configuración automática del entorno
    Crea el archivo .env si no existe con valores por defecto
    """
    print("🔧 Configurando entorno...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creando archivo .env con configuración por defecto...")
        
        # Configuración por defecto
        default_config = """# 🔐 Configuración de Base de Datos
DATABASE_URL=postgresql://parcial1web_user:SecurePass2024@shuttle.proxy.rlwy.net:31337/parcial1web

# 🔑 Configuración JWT  
JWT_SECRET_KEY=super-secret-jwt-key-change-in-production-2024

# 🌍 Configuración del Entorno
FLASK_ENV=development
FLASK_DEBUG=True

# 📝 Notas:
# - Cambia JWT_SECRET_KEY en producción por algo más seguro
# - DATABASE_URL apunta a tu base de datos PostgreSQL
# - FLASK_DEBUG=True habilita el modo debug para desarrollo
"""
        
        env_file.write_text(default_config.strip())
        print("✅ Archivo .env creado exitosamente")
    else:
        print("✅ Archivo .env ya existe")
    
    # Cargar variables de entorno desde .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Variables de entorno cargadas desde .env")
    except ImportError:
        print("⚠️  python-dotenv no instalado. Usando variables por defecto.")


def setup_database():
    """
    🗄️ Configuración automática de la base de datos
    Inicializa y crea todas las tablas necesarias
    """
    print("🗄️ Configurando base de datos...")
    
    try:
        from config.database import init_db
        init_db()
        print("✅ Base de datos inicializada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        print("💡 Verifica que:")
        print("   - La URL de la base de datos sea correcta")
        print("   - El servidor de base de datos esté ejecutándose")
        print("   - Las credenciales sean válidas")
        return False


def create_app():
    """
    🏗️ Factory para crear y configurar la aplicación Flask
    """
    print("🏗️ Creando aplicación Flask...")
    
    # Inicializar la app Flask
    app = Flask(__name__)
    
    # Configuración JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expira en 1 hora
    
    # Configuración adicional
    app.config['JSON_SORT_KEYS'] = False  # Mantener orden de JSON
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # JSON pretty print
    
    # Inicializar JWT Manager
    jwt = JWTManager(app)
    
    # Manejadores de errores JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token expirado', 'code': 'TOKEN_EXPIRED'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Token inválido', 'code': 'TOKEN_INVALID'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Token de autenticación requerido', 'code': 'TOKEN_REQUIRED'}), 401
    
    # Endpoint raíz para verificar que la API está funcionando
    @app.route('/')
    def health_check():
        """Endpoint de verificación de salud de la API"""
        return jsonify({
            'message': '🚀 Parcial1Web API funcionando correctamente',
            'version': '1.0.0',
            'status': 'healthy',
            'endpoints': {
                'authentication': '/auth/*',
                'weapons': '/weapons/*',
                'categories': '/categories/*'
            },
            'documentation': {
                'postman': 'Ver carpeta /postman/ para colección completa',
                'openapi': 'Ver /docs/openapi.yaml para especificación Swagger'
            }
        })
    
    # Endpoint de información del sistema
    @app.route('/info')
    def system_info():
        """Endpoint con información del sistema"""
        return jsonify({
            'system': 'Parcial1Web - Sistema de Autenticación',
            'features': [
                'Registro de usuarios con validación',
                'Login JWT con access y refresh tokens',
                'Gestión de armas y categorías',
                'Documentación completa Postman + OpenAPI'
            ],
            'authentication': {
                'access_token_duration': '1 hora',
                'refresh_token_duration': '30 días',
                'hash_algorithm': 'bcrypt (12 rounds)'
            },
            'database': 'PostgreSQL con SQLAlchemy ORM'
        })
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)      # Endpoints de autenticación  
    app.register_blueprint(weapons_bp)   # Endpoints de armas y categorías
    
    print("✅ Aplicación Flask configurada")
    return app


def print_startup_info():
    """
    📋 Mostrar información de inicio del sistema
    """
    print("\n" + "="*50)
    print("🎉 ¡SISTEMA INICIADO CORRECTAMENTE!")
    print("="*50)
    print("🌐 API ejecutándose en: http://localhost:5000")
    print("📚 Documentación:")
    print("   • Health check: http://localhost:5000/")
    print("   • Info sistema: http://localhost:5000/info")  
    print("   • Postman: ./postman/")
    print("   • OpenAPI: ./docs/openapi.yaml")
    print("\n🔑 Endpoints de autenticación:")
    print("   • POST /auth/register - Registro de usuario")
    print("   • POST /auth/login - Login con JWT")
    print("   • GET /auth/me - Usuario actual")
    print("   • POST /auth/refresh - Renovar token")
    print("   • POST /auth/logout - Cerrar sesión")
    print("\n🛡️ Endpoints de armas:")
    print("   • GET /categories - Listar categorías")
    print("   • POST /categories - Crear categoría")
    print("   • GET /weapons - Listar armas")
    print("   • POST /weapons - Crear arma")
    print("\n💡 Para probar rápidamente:")
    print("   1. Importar postman/Parcial1Web_Auth_Collection.json en Postman")
    print("   2. O usar: python postman/test_collection.py")
    print("\n🚀 ¡Listo para usar!")
    print("="*50)


def main():
    """
    🚀 Función principal - Auto-configura e inicia todo el sistema
    """
    print("🚀 INICIANDO PARCIAL1WEB - SISTEMA DE AUTENTICACIÓN")
    print("="*50)
    
    # Paso 1: Configurar entorno
    setup_environment()
    
    # Paso 2: Configurar base de datos
    db_success = setup_database()
    if not db_success:
        print("\n❌ No se pudo conectar a la base de datos.")
        print("💡 El sistema puede funcionar parcialmente, pero algunos endpoints fallarán.")
        response = input("\n¿Continuar de todas formas? (s/N): ")
        if response.lower() != 's':
            print("🛑 Iniciación cancelada por el usuario")
            sys.exit(1)
    
    # Paso 3: Crear aplicación Flask
    app = create_app()
    
    # Paso 4: Mostrar información de inicio
    print_startup_info()
    
    # Paso 5: Iniciar servidor Flask
    try:
        print("\n🔥 Iniciando servidor Flask...")
        app.run(
            host='0.0.0.0',  # Permitir conexiones externas
            port=5000,       # Puerto estándar
            debug=True,      # Modo debug habilitado
            use_reloader=False  # Evitar doble ejecución en debug mode
        )
    except KeyboardInterrupt:
        print("\n\n👋 Sistema detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar el servidor: {e}")
        sys.exit(1)


# 🎯 Auto-inicialización cuando se ejecuta directamente
if __name__ == '__main__':
    main()
