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

       
        query = "INSERT INTO orders (destination, origin, price, weight, user_id) VALUES (%s,%s,%s,%s,%s)"
        
        cursor_object = connection.cursor()
        cursor_object.execute(query, (data['destination'],data['origin'],data['weight']*20,data['weight'],current_userid))
        connection.commit()
        return {"message":"parcel created, waiting approval"}, 201


class GetUserParcels(Resource):
    """Class to get parcels by a specific user."""

    def get(self, user_id):
        """Get all parcel by a unique user ID."""
        current_orders=[]
        cursor_object = connection.cursor()
        query = """SELECT * FROM orders WHERE user_id= %s"""
        cursor_object.execute(query, (user_id,))
        rows = cursor_object.fetchall()
        if len(rows)==0:
            return{"error":"user {} has no parces".format(user_id)}, 404
        for row in rows:
            order = Order(*row)
            current_orders.append(order)
            return{"user {} orders".format(user_id):[order.serialize_order() for order in current_oders]}, 200

class GetParcels(Resource):
    """Class for get parcel method."""

    def get(self):
        """Get method to return all orders."""
        current_orders=[]
        cursor_object = connection.cursor()
        query = """SELECT * FROM orders """
        cursor_object.execute(query)
        rows = cursor_object.fetchall()
        if len(rows)==0:
            return{"error":"no parcels found"}, 404
        for row in rows:
            order = Order(*row)
            current_orders.append(order)
            return{"All orders":[order.serialize_order() for order in current_orders]}, 200

class ChangeParcelDestination(Resource):
    """class for changing parcel destination."""
    @jwt_required
    def put(self, order_id):
        """Put method changes parcel destination."""
        parser=reqparse.RequestParser()
        parser.add_argument("destination",help ="Invalid name check again", required=True)
        data=parser.parse_args()

        query = "UPDATE orders SET destination = %s WHERE order_id = %s"
        user_id = get_jwt_identity()
        order = Order().get_order_by_orderid(order_id)
        if order:
            if order.user_id == user_id:
                if order.status == "delivered" or order.status == "cancelled":
                    return{"error":"can't change, this already {}".format(order.status)}, 404
                cursor_object = connection.cursor()
                cursor_object.execute(query,(data['destination'],order_id,))
                connection.commit()
                return{"success":"destination changed to{}".format(data['destination'])}, 200
        return{"error":"order not found"},404

class GetSPecificParcel(Resource):
    """Class to get a specifi parcel order."""
    def get(self, order_id):
        """Get method fetch a specific parcel."""
        order = Order().get_order_by_orderid(order_id)
        if order:
            return{"message":"order {} details"[order.serialize_order()]..format(order_id)}
