"""Stores all orders in a list."""
orders = []
user_orders = []
accepted_orders = []
destinations = ['Nairobi', 'Nakuru', 'Kisumu']


class Order:
    """Contain parcel and user fuctions."""

    order_id = 1
    user_id = 1

    def __init__(self, origin=None,
                 price=None, destination=None, weight=None, status="Pending"):
        """Initialize the Order class with the required arguments."""
        self.origin = origin
        self.price = price
        self.destination = destination
        self.weight = weight
        self.id = Order.order_id
        self.status = status
        self.u_id = Order.user_id
        Order.order_id += 1

    def serialize(self):
        """Return tuple as dictionary."""
        return dict(
            id=self.id,
            origin=self.origin,
            price=self.price,
            destination=self.destination,
            weight=self.weight,
            status=self.status,
            u_id=self.u_id
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
