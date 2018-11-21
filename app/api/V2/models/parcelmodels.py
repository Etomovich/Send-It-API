"""Create a order object form the class."""

class Order:
    """Contain parcel and user fuctions."""

    def __init__(self, order_id=None, destination=None, origin=None,
                 price=None,  weight=None, status=None, user_id=None, 
                 curr_location=None):
        """Initialize the Order class with the required arguments."""
        self.origin = origin
        self.price = price
        self.destination = destination
        self.weight = weight
        self.order_id = order_id
        self.status = status
        self.curr_location = curr_location
        self.user_id=user_id
        

    def serialize(self):
        """Return tuple as dictionary."""
        return dict(
            id=self.id,
            origin=self.origin,
            price=self.price,
            destination=self.destination,
            weight=self.weight,
            status=self.status,
            u_id=self.u_id,
            curr_location=self.curr_location
        )

    def get_by_id(self, order_id):
        """Get a single item by unique id."""
        for order in orders:
            if order.id == order_id:
                return order

    def get_by_user_id(self, user_id):
        """Get all parcel by a unique user ID."""
        for order in orders:
            if order.u_id == user_id:
                user_orders.append(order)
                return user_orders
