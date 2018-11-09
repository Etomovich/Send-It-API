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
        return {"orders": [order.serialize() for order in orders]