import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # URL do banco de dados SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(Config)  # Config importado de config.py

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app import routes, models  # Importar aqui para evitar circular imports

    login_manager.login_view = 'login'

    return app
