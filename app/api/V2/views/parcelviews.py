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
            current_user_orders.append(order)
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
            current_user_orders.append(order)
            return{"All orders":[order.serialize_order() for order in current_oders]}, 200



    


class CancelSpecificParcel(Resource):
    """class forcancelling specific parcel."""

    def put(self, id):
        """Put method to change status to cancelled."""
        order = Order().get_by_id(id)

        if order:
            if order.status == ("cancelled" or "moving" or "delivered"):

                return {"message": "can't cancel,order already {}"
                        .format(order.status)}, 200
            order.status = "cancelled"
            return{"message": "parcel order cancelled succesfully"}, 200

        return {"message": "order not found"}, 404


class SpecificParcel(Resource):
    """Class for handling specific parcel endpoint."""

    def get(self, id):
        """Get method to fetch specific parcel orders."""
        order = Order().get_by_id(id)

        if order:
            return {"order": order.serialize()}, 200

        return {"message": "Order not found"}, 404

    def delete(self, id):
        """Delete method for deleting specific parcel order."""
        order = Order().get_by_id(id)

        if order:
            orders.remove(order)
            return {"message": "order deleted successfully"}, 200
        return {"message": "Order not found"}, 404


class DeclinedParcels(Resource):
    """Class for handling declined parcel orders."""

    def get(self):
        """Get method to fetch all declined parcels."""
        return {
            "declined orders": [
                order.serialize() for order in orders
                if order.status == "declined"
            ]
        }


class DeclineParcel(Resource):
    """Admin class for declining parcel order."""

    def put(self, id):
        """Put method to change parcel status to declined."""
        order = Order().get_by_id(id)

        if order:

            if order.status != "pending":
                return {"message": "order already {}".format(order.status)}

            order.status = "declined"
            return {"message": "Order declined"}

        return {"message": "Order not found"}, 404


class DeliveredParcels(Resource):
    """Return a list of parcel orders completed by admin."""

    def get(self):
        """Get method to fetch all deliverd parcels."""
        return {"completed orders": [order.serialize() for order in orders if
                order.status == "completed"]}, 200


class PendingParcels(Resource):
    """Return all pending parcels."""

    def get(self):
        """Get method fethes all pending parcels."""
        return {"Pending parcels": [order.serialize() for order in orders if
                order.status == ("pending" or "Pending")]}, 200


class MovingParcels(Resource):
    """Class to handle orders in transit(moving)."""

    def get(self):
        """Return all moving orders."""
        return {"moving parcels": [order.serialize() for order in orders if
                order.status == "In Transit"]}


class MarkParcelInTransit(Resource):
    """Admin class for marking parcel status to moving."""

    def put(self, id):
        """Put method change status to moving."""
        order = Order().get_by_id(id)

        if order:
            if order.status == ("completed" or "declined"):
                return {"You already marked the order as {}"
                        .format(order.status)}, 200

            if order.status == "pending":
                return {"message": "order should be approved first"}, 200

            if order.status == "approved":
                order.status = "moving"
                return {"message": "Parcel {}"
                        .format(id) + " now on road"}, 200

        return {"message": "order not found"}, 404


class ApproveParcel(Resource):
    """Admin class for approving parcel."""

    def put(self, id):
        """Put method change parcel status to approved."""
        order = Order().get_by_id(id)

        if order:
            if order.status != "pending":
                return {"message": "order already {}"
                        .format(order.status)}, 200
            order.status = "approved"
            return {"message": "your order has been approved"}, 200

        return {"message": "order not found"}, 404


class DeliverParcel(Resource):
    """Admin class for changing parcel status to delivered."""

    def put(self, id):
        """Put method change status to delivered."""
        order = Order().get_by_id(id)

        if order:
            if order.status == ("delivered" or "declined"):
                return {"message": "parcel already {}".format(order.status)}

            if order.status == "pending":
                return {"message": "please approve the order first "}

            if order.status == "moving":
                order.status = "delivered"
                return {
                    "message":
                    "parcel {}".format(id) + " delivered successfully"
                }

        return {"message": "Order not found"}, 404


class GetAcceptedParcels(Resource):
    """Get the Orders accepted by admin."""

    def get(self):
        """Return list of approved orders."""
        return {
            "approved_orders": [
                order.serialize() for order in orders
                if order.status == "approved"
            ]
        }, 200
