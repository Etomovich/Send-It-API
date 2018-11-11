from flask import Flask, request
from flask_restful import Resource
from .models import Order,orders, accepted_orders, destinations
from utils import valid_destination_name, valid_origin_name

class CreateParcel(Resource):
    '''place parcel order.'''

    def post(self):
        '''place a new parcel order.'''

        data = request.get_json()
        origin = data['origin']
        price = data['price']
        destination = data['destination']
        weight = data['weight']

        if not valid_destination_name(destination):
            return {'message': "destination not valid"}, 400

        if not valid_origin_name(origin):
            return {'message': "invalid origin name"}, 400

        if type(price) != int:
            return {'message': "Invalid price"}, 400

        if type(weight) != int:
            return {'message': "Invalid weight"}, 400

        order = Order(origin, price, destination, weight)

        if order.destination in destinations:
            orders.append(order)
            return {"message": "Order placed waiting for approval!"}, 201
        return {"message": "sorry we do not deliver to {}".format(order.destination)}


class GetParcels(Resource):
    def get(self):
        return {"orders": [order.serialize() for order in orders]}

class SpecificParcel(Resource):
    '''fetch a specific parcel order by id'''

    def get(self, id):
        '''get a specific order by id'''

        order = Order().get_by_id(id)

        if order:
            return {"order": order.serialize()}, 200

        return {"message": "Order not found"}, 404

    def delete(self, id):
        '''delete a specific order'''

        order = Order().get_by_id(id)

        if order:
            orders.remove(order)
            return {"message": "order deleted successfully"}, 200
        return {"message": "Order not found"}, 404

    def put(self, id):
        '''approve an  a parcel order'''
        order = Order().get_by_id(id)

        if order:
            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}, 200
            order.status = "approved"
            return {"message": "your parcel order has been approved"}, 200
        return {"message": "order not found"}, 404

class DeclinedParcels(Resource):
    def get(self):
        '''return all orders'''

        return {
            "declined orders": [
                order.serialize() for order in orders
                if order.status == "declined"
            ]
        }

class DeclineParcel(Resource):
    def put(self, id):
        '''decline a specific order'''

        order = Order().get_by_id(id)

        if order:

            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}

            order.status = "declined"
            return {"message": "Order declined"}

        return {"message": "Order not found"}, 404

class DeliveredParcels(Resource):
    '''return a list of parcel orders completed by admin'''

    def get(self):
        return {"completed orders": [order.serialize() for order in orders if order.status == "completed"]}, 200


class MovingParcels(Resource):
    def get(self):
        return {"In Transitorder": [order.serialize() for order in orders if order.status == "In Transit"]}

class MarkParcelInTransit(Resource):
    def put(self, id):
        '''mark order has started being transported'''
        order = Order().get_by_id(id)

        if order:
            if order.status == "completed" or order.status == "declined":
                return {"You already marked the order as {}".format(order.status)}, 200

            if order.status == "Pending":
                return {"message": "please approve the order first"}, 200

            if order.status == "approved":
                order.status = "In Transit"
                return {"message": "The order is now on the road!Rember to keep track of the order"}, 200

        return {"message": "The order could not be found!,check on the id please"}, 404




class AcceptStatus(Resource):
    def put(self, id):
        '''mark an order as approved'''

        order = Order().get_by_id(id)

        if order:
            if order.status != "Pending":
                return {"message": "order already {}".format(order.status)}, 200
            order.status = "approved"
            return {"message": "your order has been approved"}, 200

        return {"message": "order not found"}, 404

class CompleteOrder(Resource):
    def put(self, id):
        '''mark an order as completed by admin'''
        order = Order().get_by_id(id)

        if order:
            if order.status == "completed" or order.status == "declined":
                return {"message": "order already {}".format(order.status)}

            if order.status == "Pending":
                return {"message": "please approve the order first "}

            if order.status == "In Transit":
                order.status = "completed"
                return {
                    "message":
                    "Your has been order completed awaiting delivery"
                }

        return {"message": "Order not found"}, 404


class GetAcceptedOrders(Resource):
    '''Get the Orders accepted by admin'''

    def get(self):
        '''return list of approved orders'''

        return {
            "approved_orders": [
                order.serialize() for order in orders
                if order.status == "approved"
            ]
        }, 200

