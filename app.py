
from flask import Flask
from controllers.weapons_controller import weapons_bp
from controllers.auth_controller import auth_bp
from config.database import init_db

# Inicializar la app Flask
app = Flask(__name__)

# Inicializar la base de datos
init_db()

# Registrar blueprints
app.register_blueprint(auth_bp)      # Endpoints de autenticación
app.register_blueprint(weapons_bp)   # Endpoints de armas y categorías

if __name__ == '__main__':
	app.run(debug=True)
