#161834525
from flask import Flask
from flask_restful import Api
from config import app_config
from .orders import GetOrders, CompletedOrders, PostParcel, InTransitOrders, SpecificOrder, DeclinedOrders, MarkOrderInTransit, CompleteOrder, AcceptStatus, GetAcceptedOrders, DeclineOrder


def create_app(config_stage):
    '''creates the app'''

    app = Flask(__name__)
    app.config.from_object(app_config[config_stage])

    api = Api(app)

    api.add_resource(SpecificOrder, '/api/v1/orders/<int:id>')
    api.add_resource(PostParcel, '/api/v1/placeorder/orders')
    api.add_resource(GetOrders, '/api/v1/orders')
    api.add_resource(GetAcceptedOrders, '/api/v1/acceptedorders')
    api.add_resource(CompleteOrder, '/api/v1/orders/<int:id>/completed')
    api.add_resource(CompletedOrders, '/api/v1/orders/completedorders')
    
    api.add_resource(DeclinedOrders, '/api/v1/orders/declined')
    api.add_resource(AcceptStatus, '/api/v1/orders/<int:id>/approved')
    api.add_resource(MarkOrderInTransit, '/api/v1/orders/<int:id>/intransit')
    api.add_resource(InTransitOrders, '/api/v1/orders/intransit')
    api.add_resource(DeclineOrder, '/api/v1/orders/<int:id>/declined')

    return app
