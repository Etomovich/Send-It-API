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


class GetOrders(Resource):
    def get(self):
        return {"orders": [order.serialize() for order in orders]}

class SpecificOrder(Resource):
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

class DeclinedOrders(Resource):
    def get(self):
        '''return all orders'''

        return {
            "declined orders": [
                order.serialize() for order in orders
                if order.status == "declined"
            ]
        }