from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# 1. Creamos las extensiones SIN inicializar
# Otros archivos (como models.py) importarán 'db' desde aquí
db = SQLAlchemy()
login_manager = LoginManager()

# 2. Definimos la "fábrica" de la app
def create_app():
    app = Flask(__name__)

    # 3. Configuramos la app
    app.config['SECRET_KEY'] = 'clave_secreta_muy_dificil_de_adivinar' # ¡Cambia esto en producción!
    
    # --- Configuración de la Base de Datos ---
    # Usamos 'instance' para la DB local. Render usará DATABASE_URL
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Esta es la configuración que usará Render (DATABASE_URL)
    # y si no la encuentra, usará un archivo local 'app.db'
    db_path = os.path.join(basedir, '..', 'instance', 'app.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + db_path
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Nos aseguramos de que la carpeta 'instance' exista
    try:
        os.makedirs(os.path.join(basedir, '..', 'instance'))
    except OSError:
        pass # La carpeta ya existe
    # ----------------------------------------

    # 4. Conectamos las extensiones a la app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configuración de Flask-Login
    login_manager.login_view = 'main.login' # A dónde redirigir si no está logueado
    login_manager.login_message = 'Por favor, inicia sesión para acceder.'
    login_manager.login_message_category = 'error' # Categoría para los flashes

    # 5. Registrar Blueprints (Rutas)
    # Importamos aquí para evitar importaciones circulares
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 6. Importar modelos (para que db.create_all() los vea)
    # Hacemos esto *después* de crear 'db' y ANTES de crear las tablas
    from . import models 

    return app
