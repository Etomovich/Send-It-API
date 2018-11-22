"""Crete app."""
from flask import Flask
from .api.V1 import version_1
from .api.V2 import version_2
from app.db_config import create_orders_table,create_users_table, create_super_admin
import os
from flask_jwt_extended import JWTManager


def create_app(config):
    """Crete app fuction."""
    app = Flask(__name__)
    app.secret_key = os.getenv("secret_key") or "brian"
    create_orders_table()
    create_users_table()
    create_super_admin()
    app.register_blueprint(version_1)
    app.register_blueprint(version_2)
    jwt = JWTManager(app)

    return app
