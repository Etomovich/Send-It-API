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

        data = parser.parse_args()

        query = """INSERT INTO users (username, email, password, phone) VALUES (%s,%s,%s,%s)"""

        user = User().get_user_by_username(data['username'])
        if not user:
            cursor_object = connection.cursor() 
            cursor_object.execute(query, (data['username'], data['email'],data['password'],data['phone'],))
            connection.commit()
            user = User().get_user_by_username(data['username'])
            access_token = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(user.user_id)
            return {"access token":access_token}, 200
        
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
                access_token = create_access_token(identity=user.user_id, fresh=True)
                refresh_roken = create_refresh_token(user.user_id)
                return {"access token":access_token}, 200

            return {"message":"invalid password, try again"}, 

        return{"message":"user not found please register"}, 404

class TokenRefresh(Resource):
    """Refresh user access token."""
    def post(self):
        """Retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method."""
        user = get_jwt_identity()
        """Return a non-fresh token for the user."""
        new_token = create_access_token(identity=user, fresh=False)
        return {'refreshed token': new_token}, 200

class GetAllUsers(Resource):
    """Get all registered users."""
    def get(self):
        """Get method fetch all users."""
        current_users = []
        cur = connection.cursor()
        query = "SELECT * FROM users"
        cur.execute(query)
        rows = cur.fetchall()
        if len(rows)==0:
            return{"message":"no user found"}, 404
        for row in rows:
            user = User(*row)
            current_users.append(user)

        return {"all users":[user.serialize_user() for user in current_users]}, 200

class GetSpecificUser(Resource):
    """Get a specific user by user_id."""
    def get(self, user_id):
        """Get method return specific user."""
        user = User().get_user_by_userid(user_id)
        if user:
            return{"message":"user {} details:"user.serialize_user()}
