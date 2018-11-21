"""Contain test cases for the endpoints."""
import unittest
import json
from app import create_app


class TestAllOrders(unittest.TestCase):
    """Class for testing endpoints."""

    def setUp(self):
        """Setup method to define data."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
            "origin": "nairobi",
            "price": 200,
            "destination": "Nakuru",
            "weight": 20
        }
        self.userdata = {
        "username":"brianserems",
        "password":"idfwu8080",
        "email":"b@ushacks.com"
        }

    def tearDown(self):
        """Tear down method."""
        self.app_context.pop()




if __name__ == '__main__':

    unittest.main()
