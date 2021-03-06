"""Contain parcels view classes and methods."""
from flask_restful import Resource, reqparse
from ..models.parcelmodels import Order
from ..models.usermodels import User, connection
from ..utils import valid_destination_name, valid_origin_name
from flask_jwt_extended import (create_refresh_token,jwt_refresh_token_required,jwt_required)
from flask_jwt_extended import get_jwt_identity

class CreateParcel(Resource):
    """Create a new parcel order."""
    @jwt_required
    def post(self):
        """Post method to create a parcel."""
        current_userid = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('name', help='invalid name,it should be name', required=True)
        parser.add_argument('destination', help='invalid name, check again', required=True)
        parser.add_argument('weight', help='Invalid weight', type=int, required=True)
        parser.add_argument('origin', help='invalid name, check again', required=True)
        data = parser.parse_args()
        price = data['weight']*10

        order = Order(name=data['name'],destination=data['destination'],origin=data['origin'],price=price,weight=data['weight'],user_id=current_userid)
        if not valid_destination_name(data['destination']):
            return {'message': "invalid name, it should be destination"}, 400

        if not valid_origin_name(data['origin']):
            return {'message': "invalid name, it should be origin"}, 400

        if type(price) != int:
            return {'message': "Invalid price, it should be a number"}, 400

        if type(data['weight']) != int:
            return {'message': "Invalid weight, it should be a number"}, 400

        if current_userid:
            Order().insert_to_db(order)
            return {"status":"success","message":"your parcel has been created","details":order.serialize_order()}, 201
        return{"message":"you should first register"}, 400

        


class GetUserParcels(Resource):
    """Class to get parcels by a specific user."""
    
    @jwt_required
    def get(self, user_id):
        """Get all parcel by a unique user ID."""
        current_user = get_jwt_identity()
        user = User().get_user_by_id(current_user)
        if user.role == "admin" or user.user_id == user_id:
            user_in_db= User().get_user_by_id(user_id)
            if user_in_db:
                userparcels = Order().get_user_parcels(user_id)
                if len(userparcels) == 0:
                    return{"smessage":"user {} has no parcels".format(user_id),"message":"you have no parcels"}
                return{"message":[parcel.serialize_order() for parcel in userparcels],"status":"success"}, 200
            return{"message":"we don't have user {} in our database".format(user_id)}
        return{"message":"you are not allowed to view these,you should be admin or the owner"}, 403
        

class GetParcels(Resource):
    """Class for get parcel method."""
    
    @jwt_required
    def get(self):
        """Get method to return all orders."""
        allparcels = Order().get_all_parcels()
        if len(allparcels) == 0:
            return{"message":"no parcels found","status":"notfound"}, 404
        return{"status":"success", "message":[parcel.serialize_order() for parcel in allparcels]}, 200

class GetSpecificParcel(Resource):
    """Class to get a specifi parcel order."""

    @jwt_required
    def get(self, order_id):
        """Get method fetch a specific parcel."""
        order = Order().get_order_by_orderid(order_id)
        if order:
            return{"message":order.serialize_order(),"status":"success"},200
        return{"message":"order {} not found".format(order_id)}, 404

class GetStatusParcels(Resource):
    """Class to get all delivered parcels."""

    @jwt_required
    def post(self):
        """Get method to return all delivered parcels."""
        user_id = get_jwt_identity()
        user = User().get_user_by_id(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('status', help='invalid name,it should be status', required=True)
        data = parser.parse_args()
        status = data['status']
        if user.role == "admin":
            orders = Order().get_specific_parcels(status)
            if orders:
                return{"message":[order.serialize_order() for order in orders]},200
            return{"message":"no {} parcels found".format(status)},204
        return{"message":"you should be an admin to view {} parcels".format(status)},403
        


class ChangeParcelStatus(Resource):
    """Admin class to change parcel status."""
    @jwt_required
    def put(self, order_id):
        """Put method updates parcel status."""

        parser=reqparse.RequestParser()
        parser.add_argument("new status",help ="Invalid, it should be new status", required=True)
        data=parser.parse_args()
        current_userid = get_jwt_identity()

        user = User().get_user_by_id(current_userid)
        if user:
            if user.role == "admin":
                order = Order().get_order_by_orderid(order_id)
                if order:
                    if order.status ==  "cancelled" or order.status ==  "delivered":
                        return{"message":"can't change to {}".format(data['new status'])+" this already {}".format(order.status)}, 409
                    Order().change_parcel_status(data['new status'], order_id)
                    return{"message":"parcel status changed to {}".format(data['new status'])}, 200
                return{"message":"order not found"},404
            return {"message":"you are not an admin"}, 403
        return{"message":"user not found"}, 404

class ChangeParcelLocation(Resource):
    """Class for admin, changing parcel location."""
    
    @jwt_required
    def put(self, order_id):
        """Put method update current location."""
        parser=reqparse.RequestParser()
        parser.add_argument("new location",help ="Invalid, it should be new location", required=True)
        data=parser.parse_args()
        current_userid = get_jwt_identity()
        newlocation = data['new location']
        user = User().get_user_by_id(current_userid)
        if user:
            if user.role == "admin":
                order = Order().get_order_by_orderid(order_id)
                if order:
                    Order().change_parcel_location(newlocation, order_id)
                    return{"message":"admin changed location to {}:".format(newlocation)}, 200
                return{"message":"order not found"},404
            return {"message":"you are not an admin"}, 403
        return{"message":"user not found"}, 404

class ChangeParcelDestination(Resource):
    """class for changing parcel destination."""

    @jwt_required
    def put(self, order_id):
        """Put method changes parcel destination."""
        parser=reqparse.RequestParser()
        parser.add_argument("destination",help ="Invalid name check again", required=True)
        data=parser.parse_args()
        user_id = get_jwt_identity()
        order = Order().get_order_by_orderid(order_id)
        if order:
            if order.user_id == user_id:
                if order.status == "delivered" or order.status == "cancelled":
                    return{"message":"can't change, this already {}".format(order.status)}, 409
                Order().change_parcel_destination(data['destination'])
                return{"message":"destination changed to{}".format(data['destination'])}, 200
            return{"message":"not allowed, only owners may change parcel destination"}, 403
        return{"message":"order not found"},404
