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

    @classmethod
    def get_order_by_orderid(cls, order_id):
        """Find an order by order_id."""
        cursor_object = connection.cursor()
        query = """SELECT * FROM orders WHERE order_id= %s"""
        cursor_object.execute(query, (order_id,))
        row = cursor_object.fetchone()
        if row:
            order = cls(*row)
        else:
            order = None
        return order

    