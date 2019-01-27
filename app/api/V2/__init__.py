"""Contain urls and blueprint."""
from flask import Blueprint
from flask_restful import Api
from .views.parcelviews import GetParcels, CreateParcel
from .views.parcelviews import GetUserParcels,GetSpecificParcel
from .views.parcelviews import ChangeParcelLocation, GetStatusParcels
from .views.parcelviews import ChangeParcelDestination, ChangeParcelStatus
from .views.userviews import UserRegistration, TokenRefresh, UserLogOut
from .views.userviews import GetAllUsers, UserLogin, GetSpecificUser

version_2 = Blueprint('v2', __name__)

api = Api(version_2, prefix="/api/v2")

api.add_resource(GetSpecificParcel, '/parcels/<int:order_id>')
api.add_resource(CreateParcel, '/parcels')
api.add_resource(GetParcels, '/parcels')
api.add_resource(GetUserParcels, '/users/<int:user_id>/parcels')
api.add_resource(GetSpecificUser, '/users/<int:user_id>')
api.add_resource(GetStatusParcels, '/parcels/status')
api.add_resource(UserRegistration, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(TokenRefresh, '/auth')
api.add_resource(GetAllUsers, '/users')
api.add_resource(UserLogOut, '/auth/logout')
api.add_resource(ChangeParcelDestination, '/parcels/<int:order_id>/destination')
api.add_resource(ChangeParcelStatus, '/parcels/<int:order_id>/status')
api.add_resource(ChangeParcelLocation, '/parcels/<int:order_id>/presentlocation')
