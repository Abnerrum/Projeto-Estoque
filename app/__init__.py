from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar esta página."
login_manager.login_message_category = "warning"


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth_bp
    from app.routes.produtos import produtos_bp
    from app.routes.movimentacoes import mov_bp
    from app.routes.relatorios import rel_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(mov_bp)
    app.register_blueprint(rel_bp)

    return app
