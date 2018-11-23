"""Create a order object form the class."""
import psycopg2
from flask import app
from app.db_config import init_db

connection = init_db()
cursor_object = connection.cursor()

class Order:
    """Contain parcel and user fuctions."""

    def __init__(self, order_id=None, name=None, destination=None, origin=None,
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
        self.name = name
        

    def serialize_order(self):
        """Return tuple as dictionary."""
        return dict(
            id=self.order_id,
            description = self.name,
            origin=self.origin,
            price=self.price,
            destination=self.destination,
            weight=self.weight,
            status=self.status,
            user_id=self.user_id,
            curr_location=self.curr_location
        )

    @classmethod
    def get_order_by_orderid(cls, order_id):
        """Find an order by order_id."""
        query = """SELECT * FROM orders WHERE order_id= %s"""
        cursor_object.execute(query, (order_id,))
        row = cursor_object.fetchone()
        if row:
            order = cls(*row)
        else:
            order = None
        return order

    def insert_to_db(self, order_data):
        query = "INSERT INTO orders (name,destination, origin, price, weight, user_id) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor_object.execute(query, (order_data[0],order_data[1],order_data[2],order_data[3],order_data[4],order_data[5]))
        connection.commit()

    def get_user_parcels(self,user_id):
        current_user_parcels = []
        query = """SELECT * FROM orders WHERE user_id= %s"""
        cursor_object.execute(query, (user_id,))
        rows = cursor_object.fetchall()
        for row in rows:
            order = Order(*row)
            current_user_parcels.append(order)
        return current_user_parcels

    def get_all_parcels(self):
        allparcels = []
        query = """SELECT * FROM orders """
        cursor_object.execute(query)
        rows = cursor_object.fetchall()
        for row in rows:
            order = Order(*row)
            allparcels.append(order)
        return allparcels

    def change_parcel_destination(self,destination,order_id):
        query_destination = "UPDATE orders SET destination = %s WHERE order_id = %s"
        cursor_object.execute(query_destination,(destination,order_id,))
        connection.commit()
        
    def change_parcel_status(self,status,order_id):
        query_status = "UPDATE orders SET status = %s WHERE order_id = %s"
        cursor_object.execute(query_status,(status,order_id,))
        connection.commit()

    def change_parcel_location(self, location, order_id):
        query = "UPDATE orders set curr_location = %s WHERE order_id = %s"
        cursor_object.execute(query,(location, order_id,))
