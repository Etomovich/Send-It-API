import unittest
import json
from flask import Flask
from app import create_app


class TestAllOrders(unittest.TestCase):
    def setUp(self):
        '''set the app for testing
        setting a test client for testing'''

        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        self.data = {
            "origin": "nairobi",
            "price": 200,
            "destination": "nakuru",
            "weight": 20
        }

    def tearDown(self):

        self.app_context.pop()

    def test_create_parcel(self):
        '''test place a parcel order'''
        

        res = self.client.post(
            "api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)[
                         'message'], "parcel placed")

    def test_get_all_orders(self):
        '''get all placed orders'''

        res = self.client.get(
            "api/v1/parcels",
            headers={"content-type": "application/json"}
        )
        print(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_orders_in_transit(self):
        """ return a list of orders in transit """

        res = self.client.get(
            "/api/v1/parcels/moving",
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 200)

    def test_order_by_id(self):
        '''get parcel order by id'''

        res = self.client.get(
            "api/v1/parcels/1",data=json.dumps(self.data),
            headers={"content-type": "application/json"}
        )

        print(res.data)
        self.assertEqual(res.status_code, 200)

    def test_mark_parcel_as_delivered(self):
        '''test for parcel orders completed by admin'''

        res = self.client.put(
            "api/v1/parcels/1/delivered",data=json.dumps(self.data),

            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'message'], "please approve the order first ")

    def test_declined_parcels_by_admin(self):
        '''test for returning a list of parcel orders declined by admin'''

        res = self.client.get(
            "api/v1/parcels/declined",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_create_parcel(self):
        '''method to post an order'''
        data = {
            "origin": "kiambu",
            "price": 20,
            "destination": "nakuru",
            "weight": 25
        }
        res = self.client.post(
            "api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json"}
        )
        return res

    def test_cancel_parcel(self):
        '''test for deleting an order'''
        res = self.client.delete(
            "api/v1/parcels/1",data=json.dumps(self.data),
            headers={"content-type": "application/json"}

        )
        self.assertEqual(res.status_code, 200)

    def test_get_accepted_parcels(self):
        '''test for getting a list of all orders accepted by admin'''

        res = self.client.get(
            "api/v1/parcels/delivered",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_update_status_approved(self):
        '''test for a parcel order whose status has been approved'''

        res = self.client.put(
            "api/v1/parcels/1/approved",data=json.dumps(self.data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'message'], "your order has been approved")

    def test_completed_orders(self):
        '''test for returning a list of completed orders'''

        res = self.client.get(
            "api/v1/parcels/delivered",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_non_order_by_id(self):
        '''testing for a an order that doesn't exist'''

        res = self.client.get(
            "api/v1/parcels/345",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Order not found")

    def test_non_order_delete(self):
        '''deleting an order that doesn't exist'''

        res = self.client.delete(
            "api/v1/parcels/156",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Order not found")

    def test_declined_orders_list(self):
        '''testing for declined order'''

        res = self.client.get(
            "api/v1/parcels/declined",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_mark_order_as_in_transit(self):
        '''test for parcel orders marked intransit by admin'''

        res = self.client.put(
            "api/v1/parcels/2/moving",

            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)[
                         'message'], "please approve the order first")

    def test_decline_an_order(self):
        '''test for declining an order'''
        res = self.client.put(
            "api/v1/parcels/1/declined",data=json.dumps(data),
            headers = {"content-type": "application/json"}
        )
        self.assertEqual(res.status_code,200)

    def test_invalid_origin_name(self):
        '''test for invalid origin name'''
        data = {
            "origin": "******",
            "price": 20,
            "destination": "kiambu",
            "weight": 5
        }

        res = self.client.post(
            "api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "invalid origin name")

    def test_invalid_destination(self):
        '''test for invalid destination'''
        data = {
            "origin": "nairobi",
            "price": 20,
            "destination": "!!!!!!!",
            "weight": 5
        }

        res = self.client.post(
            "api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)[
                         'message'], "destination not valid")

    def test_invalid_price(self):
        '''test for invalid  price'''
        data = {
            "origin": "kiambu",
            "price": "kevo",
            "destination": "kiambu",
            "weight": 5
        }

        res = self.client.post(
            "api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)['message'], "Invalid price")

    def test_invalid_weight(self):
        '''test for invalid  price'''
        data = {
            "origin": "kiambu",
            "price": 50,
            "destination": "kiambu",
            "weight": "vdhdsfd"
        }

        res = self.client.post(
            "api/v1/parcels",
            data=json.dumps(data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)['message'], "Invalid weight")


if __name__ == '__main__':

    unittest.main()
