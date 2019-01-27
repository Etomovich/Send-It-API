"""Crete app."""
from flask import Flask, request, jsonify
from flask_cors import CORS
from .api.V1 import version_1
from .api.V2 import version_2
from app.db_config import (create_orders_table,create_users_table, create_super_user,
    create_super_admin,create_revokedtoken_table)
import os
import datetime
from flask_jwt_extended import JWTManager
from app.api.V2.models.usermodels import RevokedTokenModel



def create_app(config):
    """Crete app fuction."""
    app = Flask(__name__)
    CORS(app)

    app.secret_key = os.getenv("secret_key") or "brian"
    app.config['JWT_SECRET_KEY'] = 'super-secret' 
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=6) 



    app.register_blueprint(version_1)
    app.register_blueprint(version_2)

    jwt = JWTManager(app) 
    
    create_orders_table()
    create_users_table()
    create_super_admin()
    create_super_user()
    create_revokedtoken_table()

    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Origin', '*')
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Overwrite, Destination, Content-Type, Depth, User-Agent, Translate, Range, Content-Range, Timeout, X-File-Size, X-Requested-With, If-Modified-Since, X-File-Name, Cache-Control, Location, Lock-Token, If')        
    #     response.headers.add('Access-Control-Expose-Headers', 'DAV, content-length, Allow')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    #     return response
    
    
    @jwt.expired_token_loader
    def my_expired_token_callback(expired_token):
        token_type = expired_token['type']
        return jsonify({
            'status': 401,
            'sub_status': 42,
            'smessage': 'The {} token has expired'.format(token_type),
            'message':'Your session has expired, log in again'
            }), 401
    
    @jwt.token_in_blacklist_loader
    def if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel().check_token_if_blacklisted(jti)

    @jwt.revoked_token_loader
    def my_revoked_token_callback():
        return jsonify({
        'status': 401,
        'message':'you already logged out, please log in',
        'smesage':'token alredy revoked'
        }), 401



    return app
