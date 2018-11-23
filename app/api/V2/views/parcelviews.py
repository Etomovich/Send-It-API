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

        order = (data['name'],data['destination'],data['origin'],price,data['weight'],current_userid)
        if not valid_destination_name(data['destination']):
            return {'message': "invalid name, it should be destination"}, 400

        if not valid_origin_name(data['origin']):
            return {'message': "invalid name, it should be origin"}, 400

        if type(price) != int:
            return {'message': "Invalid price, it should be a number"}, 400

        if type(data['weight']) != int:
            return {'message': "Invalid weight, it should be a number"}, 400

        Order().insert_to_db(order)
        return {"parcel created":"your parcel has been created"}, 201


class GetUserParcels(Resource):
    """Class to get parcels by a specific user."""
    
    @jwt_required
    def get(self, user_id):
        """Get all parcel by a unique user ID."""
        userid = get_jwt_identity()
        user = User().get_user_by_id(user_id)
        if user.role == "admin" or user.user_id == user_id:
            userparcels = Order().get_user_parcels(user_id)
            if len(userparcels) == 0:
                return{"error":"user {} has no parcels".format(user_id)}, 404
            return{"user {} orders".format(user_id):[parcel.serialize_order() for parcel in userparcels]}, 200
        return{"error":"you are not allowed to view these,you should be admin or the owner"}
        

class GetParcels(Resource):
    """Class for get parcel method."""
    
    @jwt_required
    def get(self):
        """Get method to return all orders."""
        allparcels = Order().get_all_parcels()
        if len(allparcels) == 0:
            return{"error":"no parcels found"}
        return{"all orders":[parcel.serialize_order() for parcel in allparcels]}, 200

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
                    return{"error":"can't change, this already {}".format(order.status)}, 404
                Order().change_parcel_destination(data['destination'])
                return{"success":"destination changed to{}".format(data['destination'])}, 200
            return{"error":"not allowed, only owners may change parcel destination"}
        return{"error":"order not found"},404

class GetSpecificParcel(Resource):
    """Class to get a specifi parcel order."""

    @jwt_required
    def get(self, order_id):
        """Get method fetch a specific parcel."""
        order = Order().get_order_by_orderid(order_id)
        if order:
            return{"order {} details".format(order_id):order.serialize_order()}
        return{"error":"order {} not found".format(order_id)}


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
                        return{"error":"can't {}".format(data['new status'])+" this already {}".format(order.status)}, 400
                    Order().change_parcel_status(data['new status'], order_id)
                    return{"message":"parcel status changed to {}".format(data['new status'])}
                return{"error":"order not found"},404
            return {"error":"you are not an admin"}, 403
        return{"error":"user not found"}, 404

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
                    return{"alert":"admin changed location to {}:".format(newlocation)}, 200
                return{"error":"order not found"},404
            return {"error":"you are not an admin"}, 403
        return{"error":"user not found"}, 404
