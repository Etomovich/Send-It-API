"""Contain views for users."""
from flask_restful import Resource, reqparse
from ..models.usermodels import  connection, User
from flask_jwt_extended import (create_access_token, get_jwt_identity)
from flask_jwt_extended import (create_refresh_token,jwt_refresh_token_required,jwt_required)


class UserRegistration(Resource):
    """Class creates user registration method."""

    def post(self):
        """Get method fetch user data."""
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='invalid name, check again', required = True)
        parser.add_argument('email', help='invalid name, check again', required = True)
        parser.add_argument('password', help='invalid name, check again', required = True)
        parser.add_argument('phone', help='invalid name, check again', required= True)
        parser.add_argument('role', help='invalid name, check again', required= True)

        data = parser.parse_args()

        query = """INSERT INTO users (username, email, password, phone, role) VALUES (%s,%s,%s,%s,%s)"""

        user = User().get_user_by_username(data['username'])
        if not user:
            try:
                cursorobject = connection.cursor() 
                curobject.execute(query, (data['username'], data['email'],data['password'],data['phone'],data['role']))
                connection.commit()
                user = User().get_by_user_username(data['username'])
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access token":access_token}, 201
                
            except:
                return {"error":"error connecting to the database"}, 404
        
        return{"error":"username {} is already taken".format(data['username'])}, 404

class UserLogin(Resource):
    """Class for login in users."""

    def post(self):
        """Method for capturing user info."""
        parser=reqparse.RequestParser()
        parser.add_argument('username', help = 'invalid name, check again', required = True)
        parser.add_argument('password', help = 'invalid name, check again', required = True)
        data = parser.parse_args()
        username = data['username']
        password = data['password']

        user = User().get_user_by_username(username)
        if user:
            if password == user.password:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_roken = create_refresh_token(user.id)
                return {"access token":access_token}, 200

            return {"message":"invalid password, try again"}, 

        return{"message":"user not found please register"}, 404
