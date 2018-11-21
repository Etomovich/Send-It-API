"""Crete app."""
from flask import Flask
from .api.V1 import version_1
from .api.V2 import version_2
from app import db_config
from flask_jwt_extended import JWTManager


def create_app():
    """Crete app fuction."""
    app = Flask(__name__)
    app.secret_key = "brian"
    db_config.create_orders_table()
    db_config.create_users_table()
    app.register_blueprint(version_1)
    app.register_blueprint(version_2)
    jwt = JWTManager(app)

    return app
