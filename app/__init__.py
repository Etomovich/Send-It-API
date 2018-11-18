"""Crete app."""
from flask import Flask
from .api.V1 import version_1
from .api.V2 import version_2
from db_config import create_orders_table, create_users_table


def create_app():
    """Crete app fuction."""
    app = Flask(__name__)
    create_orders_table()
    create_users_table()
    app.register_blueprint(version_1)
    app.register_blueprint(version_2)

    return app
