
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from controllers.weapons_controller import weapons_bp
from controllers.auth_controller import auth_bp
from config.database import init_db
from datetime import timedelta

# Inicializar la app Flask
app = Flask(__name__)

# Configuración JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expira en 1 hora

# Inicializar JWT Manager
jwt = JWTManager(app)

# Manejadores de errores JWT
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {'error': 'Token expirado'}, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {'error': 'Token inválido'}, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {'error': 'Token de autenticación requerido'}, 401

# Inicializar la base de datos
init_db()

# Registrar blueprints
app.register_blueprint(auth_bp)      # Endpoints de autenticación
app.register_blueprint(weapons_bp)   # Endpoints de armas y categorías

if __name__ == '__main__':
	app.run(debug=True)
