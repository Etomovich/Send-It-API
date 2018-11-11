#161834525
from flask import Flask ,Blueprint
from flask_restful import Api
from .views.views import GetParcels,  DeliveredParcels, CreateParcel, MovingParcels, SpecificParcel, DeclinedParcels, MarkParcelInTransit, DeliverParcel, ApproveParcel, GetAcceptedParcels, DeclineParcel

version_1 = Blueprint('v1',__name__) 


    
api = Api(version_1,prefix = "/api/v1")

api.add_resource(SpecificParcel, '/parcels/<int:id>')
api.add_resource(CreateParcel, '/parcels')
api.add_resource(GetParcels, '/parcels')
api.add_resource(GetAcceptedParcels, '/parcels/accepted')
api.add_resource(DeliveredParcels, '/parcels/delivered')
api.add_resource(DeclinedParcels, '/parcels/declined')
api.add_resource(MovingParcels, '/parcels/moving')

api.add_resource(DeliverParcel, '/parcels/<int:id>/delivered')
api.add_resource(ApproveParcel, '/parcels/<int:id>/approved')
api.add_resource(MarkParcelInTransit, '/parcels/<int:id>/moving')
api.add_resource(DeclineParcel, '/parcel/<int:id>/declined')



# GET /parcels Fetch all parcel delivery orders
# GET /parcels/<parcelId> Fetch a specific parcel delivery order
# GET /users/<userId>/parcels Fetch all parcel delivery orders by a specific
# user
# PUT /parcels/<parcelId>/cancel Cancel the specific parcel delivery order
# POST /parcels Create a parcel delivery order
