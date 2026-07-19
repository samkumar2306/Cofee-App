from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.api.health import health_bp
from app.api.auth import auth_bp
from app.extensions import db, migrate, jwt
from app.middleware.error_handler import register_error_handlers
from app.api.student import student_bp
from app.api.teacher import teacher_bp

import app.models


def create_app():


    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    migrate.init_app(app, db)

    jwt.init_app(app)

    register_error_handlers(app)

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(student_bp, url_prefix="/api/students")
    app.register_blueprint(teacher_bp)

    return app