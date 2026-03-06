from flask import Flask
from .extensions import db, login_manager, migrate
from .routes.auth import auth_bp
from app.routes.papers import papers_bp 
from .routes.admin import admin_bp, dashboard_bp  # import both

from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(papers_bp, url_prefix="/papers")
    app.register_blueprint(admin_bp)         # admin routes
    app.register_blueprint(dashboard_bp)     # dashboard routes

    return app