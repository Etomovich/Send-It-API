from flask import  Blueprint,Flask
from .api.V1 import version_1


def create_app():
    app = Flask(__name__)
    app.register_blueprint(version_1)

    return app
nnvfv
 