from flask import Flask, redirect, url_for, render_template
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

    @app.route("/")
    def home():
        from .models import Paper

        recent_papers = Paper.query.order_by(Paper.created_at.desc()).limit(4).all()
        total_papers = Paper.query.count()
        verified_count = Paper.query.filter_by(verified=True).count()

        return render_template(
            "home.html",
            recent_papers=recent_papers,
            total_papers=total_papers,
            verified_count=verified_count,
        )

    return app