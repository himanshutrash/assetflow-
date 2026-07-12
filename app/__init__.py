import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please sign in to continue."
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    """Create a default Admin account on first run so there's always a way in."""
    from app.models import User, ROLE_ADMIN

    if User.query.filter_by(role=ROLE_ADMIN).first() is None:
        admin = User(name="Admin", email="admin@assetflow.local", role=ROLE_ADMIN)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
