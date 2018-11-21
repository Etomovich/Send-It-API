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

        user = User().get_by_username(data['username'])
        if not user:
            cur = connection.cursor() 
            cur.execute(query, (data['username'], data['email'],data['password'],data['phone'],data['role']))
            connection.commit()
            user = User().get_by_username(data['username'])
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access token":access_token}, 200
            return {"error":"error connecting to the database"}, 404

        return{"error":"username {} is already taken".format(data['username'])}