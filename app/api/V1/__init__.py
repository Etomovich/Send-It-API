#161834525
from flask import Flask ,Blueprint
from flask_restful import Api
from instance import *
from .views import GetOrders,  DeliveredOrders, CreateParcel, InTransitOrders, SpecificOrder, DeclinedOrders, MarkOrderInTransit, CompleteOrder, AcceptStatus, GetAcceptedOrders, DeclineOrder

version_1 = Blueprint('v1',__name__) 


    
api = Api(version_1,prefix = "/api/v1")

api.add_resource(SpecificOrder, '/orders/<int:id>')
api.add_resource(CreateParcel, '/parcels')
api.add_resource(GetOrders, '/orders')
api.add_resource(GetAcceptedOrders, '/acceptedorders')
api.add_resource(CompleteOrder, '/orders/<int:id>/completed')
api.add_resource(DeliveredOrders, '/orders/completedorders')
    
api.add_resource(DeclinedOrders, '/orders/declined')
api.add_resource(AcceptStatus, '/orders/<int:id>/approved')
api.add_resource(MarkOrderInTransit, '/orders/<int:id>/intransit')
api.add_resource(InTransitOrders, '/orders/intransit')
api.add_resource(DeclineOrder, '/orders/<int:id>/declined')



# GET /parcels Fetch all parcel delivery orders
# GET /parcels/<parcelId> Fetch a specific parcel delivery order
# GET /users/<userId>/parcels Fetch all parcel delivery orders by a specific
# user
# PUT /parcels/<parcelId>/cancel Cancel the specific parcel delivery order
# POST /parcels Create a parcel delivery order
