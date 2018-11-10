#161834525
from flask import Flask ,Blueprint
from flask_restful import Api
from instance import *
from .views import GetOrders, CompletedOrders, CreateParcel, InTransitOrders, SpecificOrder, DeclinedOrders, MarkOrderInTransit, CompleteOrder, AcceptStatus, GetAcceptedOrders, DeclineOrder

version_1 = Blueprint('v1',__name__) 

def create_app(config_stage):
    '''creates the app'''

    app = Flask(__name__)
    app.config.from_object(app_config[config_stage])

    
    api = Api(version_1,prefix = "/api/v1")

    api.add_resource(SpecificOrder, '/api/v1/orders/<int:id>')
    api.add_resource(CreateParcel, '/parcels')
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

# GET /parcels Fetch all parcel delivery orders
# GET /parcels/<parcelId> Fetch a specific parcel delivery order
# GET /users/<userId>/parcels Fetch all parcel delivery orders by a specific
# user
# PUT /parcels/<parcelId>/cancel Cancel the specific parcel delivery order
# POST /parcels Create a parcel delivery order
