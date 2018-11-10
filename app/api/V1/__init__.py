#161834525
from flask import Flask ,Blueprint
from flask_restful import Api
from instance import *
from .views import GetOrders,  DeliveredOrders, CreateParcel, InTransitOrders, SpecificOrder, DeclinedOrders, MarkOrderInTransit, CompleteOrder, AcceptStatus, GetAcceptedOrders, DeclineOrder

version_1 = Blueprint('v1',__name__) 


    
api = Api(version_1,prefix = "/api/v1")

api.add_resource(SpecificParcel, '/parcels/<int:id>')
api.add_resource(CreateParcel, '/parcels')
api.add_resource(GetParcels, '/parcels')
api.add_resource(GetAcceptedParcels, '/acceptedparcels')
api.add_resource(DeliverParcel, '/parcels/<int:id>/Delivered')
api.add_resource(DeliveredOrders, '/parcels/delivered')
    
api.add_resource(DeclinedOrders, '/parcels/declined')
api.add_resource(AcceptStatus, '/parcels/<int:id>/approved')
api.add_resource(MarkOrderInTransit, '/parcels/<int:id>/moving')
api.add_resource(InTransitOrders, '/parcels/moving')
api.add_resource(DeclineParcel, '/parcel/<int:id>/declined')



# GET /parcels Fetch all parcel delivery orders
# GET /parcels/<parcelId> Fetch a specific parcel delivery order
# GET /users/<userId>/parcels Fetch all parcel delivery orders by a specific
# user
# PUT /parcels/<parcelId>/cancel Cancel the specific parcel delivery order
# POST /parcels Create a parcel delivery order
