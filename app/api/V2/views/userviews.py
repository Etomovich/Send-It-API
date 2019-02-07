"""Contain views for users."""
from flask_restful import Resource, reqparse
from ..models.usermodels import  User, RevokedTokenModel
from flask_jwt_extended import (create_access_token, get_jwt_identity,get_raw_jwt)
from flask_jwt_extended import (create_refresh_token,jwt_refresh_token_required,jwt_required)
from ..utils import valid_destination_name, valid_email, valid_person_name
from passlib.hash import sha256_crypt


class UserRegistration(Resource):
    """Class creates user registration method."""

    def post(self):
        """Get method fetch user data."""
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='invalid name, it should be username', required = True)
        parser.add_argument('email', help='invalid name, it should be email', required = True)
        parser.add_argument('password', help='invalid name, it should be password', required = True)

        data = parser.parse_args()
        password = sha256_crypt.encrypt(data['password'])
        user = User(username=data['username'], email=data['email'],password=password)
        existing_user = user.get_user_by_username(user.username)
        if not existing_user:
            
            if not valid_person_name(data['username']):
                return {'message': "your username should contain letters and numbers only"}, 400
            if not valid_email(data['email']):
                return{"message":"your email is not valid, should be in name@domain.com format"}, 400
            User().insert_into_db(user)
            user = User().get_user_by_username(data['username'])
            if user:
                access_token = create_access_token(identity=user.user_id, fresh=True)
                refresh_token = create_refresh_token(user.user_id)
                return {"access_token":access_token, "status":"success","user_id":user.user_id,"email":user.email,"role":user.role}, 200
            return{"message":"unable to sign you up at this time","smessage":"error adding user to the datatabse"},400
        return{"message":"username {} is already taken".format(data['username'])}, 404

class UserLogin(Resource):
    """Class for login in users."""
    
    def post(self):
        """Method for capturing user info."""
        parser=reqparse.RequestParser()
        parser.add_argument('username', help = 'invalid name, it should be username', required = True)
        parser.add_argument('password', help = 'invalid name, it should be password', required = True)
        data = parser.parse_args()
        username = data['username']
        password = data['password']

        user = User().get_user_by_username(username)
        if user:
            if sha256_crypt.verify(password, user.password):
                access_token = create_access_token(identity=user.user_id, fresh=True)
                refresh_roken = create_refresh_token(user.user_id)
                return {"access_token":access_token,"status":"success","user_id":user.user_id,"role":user.role,"email":user.email}, 200

            return {"message":"invalid password try again"},400

        return{"message":"user not found ,please register"},404


class UserLogOut(Resource):
    """Class got logout endpoint."""
    
    @jwt_required
    def post(self):
        """Post method create revoke token."""
        jti = get_raw_jwt()['jti']

        try:
            revokedtoken = RevokedTokenModel(jti = jti)
            revokedtoken.add_to_blacklist(revokedtoken.jti)
            return {"message":"logged out successfully",
                    "smessage":"token revoked successfully","status":"success"}, 200
        except:
            return {"message":"there was an error logging you out",
                    "smessage":"error revoking token","status":"failed"},500


class TokenRefresh(Resource):
    """Refresh user access token."""

    def post(self):
        """Retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method."""
        user = get_jwt_identity()
        """Return a non-fresh token for the user."""
        new_token = create_access_token(identity=user, fresh=False)
        return {'refreshed_token': new_token}, 200

class GetAllUsers(Resource):
    """Get all registered users."""

    @jwt_required
    def get(self):
        """Get method fetch all users."""
        current_users = User().get_all_users()
        return {"status":"success","message":[user.serialize_user() for user in current_users]}, 200

class GetSpecificUser(Resource):
    """Get a specific user by user_id."""

    @jwt_required
    def get(self, user_id):
        """Get method return specific user."""
        user = User().get_user_by_id(user_id)
        if user:
            return{"message": user.serialize_user()}, 200
        return{"message":"user {} not found".format(user_id)}, 400
