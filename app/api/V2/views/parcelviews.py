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
        parser.add_argument('destination', help='invalid name, check again', required=True)
        parser.add_argument('weight', help='Invalid weight', type=int, required=True)
        parser.add_argument('origin', help='invalid name, check again', required=True)
        data = parser.parse_args()
        price = data['weight']*10

        order = (data['destination'],data['origin'],data['weight']*20,data['weight'],current_userid)
        if not valid_destination_name(destination):
            return {'message': "destination is invalid"}, 400

        if not valid_origin_name(origin):
            return {'message': "invalid origin name"}, 400

        if type(price) != int:
            return {'message': "Invalid price"}, 400

        if type(weight) != int:
            return {'message': "Invalid weight"}, 400

        Order().insert_into_db(order)
        return {"message":"parcel created, waiting approval"}, 201


class GetUserParcels(Resource):
    """Class to get parcels by a specific user."""
    
    @jwt_required
    def get(self, user_id):
        """Get all parcel by a unique user ID."""
        userparcels = get_user_parcels(user_id)
        if len(userparcels) == 0:
            return{"error":"user {} has no parcels"}
        return{"user {} orders".format(user_id):[order.serialize_order() for parcel in userparcels]}, 200

        

class GetParcels(Resource):
    """Class for get parcel method."""
    
    @jwt_required
    def get(self):
        """Get method to return all orders."""
        allparcels = Order().get_all_parcels()
        if len(allparcels) == 0:
            return{"error":"no parcels found"}
        return{"All orders":[parcel.serialize_order() for parcel in allparcels]}, 200

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
        return{"error":"order not found"},404

class GetSpecificParcel(Resource):
    """Class to get a specifi parcel order."""

    @jwt_required
    def get(self, order_id):
        """Get method fetch a specific parcel."""
        order = Order().get_order_by_orderid(order_id)
        if order:
            return{"message":"order {} details"[order.serialize_order()].format(order_id)}


class ChangeParcelStatus(Resource):
    """Admin class to change parcel status."""
    @jwt_required
    def put(self, order_id):
        """Put method updates parcel status."""

        parser=reqparse.RequestParser()
        parser.add_argument("newstatus",help ="Invalid name check again", required=True)
        data=parser.parse_args()
        current_userid = get_jwt_identity()

        user = get_user_by_userid(current_userid)
        if user:
            if user.role == "admin":
                order = Order().get_order_by_orderid(order_id)
                if order:
                    Order().change_parcel_status(data['newstatus'])
                    return{"message":"parcel status changed to {}".format(data['newstatus'])}
                return{"error":"order not found"},404
            return {"error":"you are not an admin"}, 402
        return{"error":"user not found"}, 404
