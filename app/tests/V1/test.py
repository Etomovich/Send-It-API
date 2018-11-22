"""Contain test cases for the endpoints."""
import unittest
import json
from app import create_app


class TestAllOrders(unittest.TestCase):
    """Class for testing endpoints."""

    def setUp(self):
        """Setup method to define data."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
            "origin": "nairobi",
            "price": 200,
            "destination": "Nakuru",
            "weight": 20
        }

    def tearDown(self):
        """Tear down method."""
        self.app_context.pop()

    def test_create_parcel(self):
        """Test create_parcel endpoint."""
        res = self.client.post(
            "api/v1/parcels",
            data=json.dumps(self.data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Order placed waiting for approval!")

    def test_cancel_order(self):
        """Test cancelling an order."""
        res = self.client.put(
            "api/v1/parcels/<int:id>/cancel",
            data=json.dumps(self.data),
            headers={"content-type": "application/json"})

        self.assertEqual(res.status_code, 404)

    def test_get_all_orders(self):
        """Test get all orders endpoint."""
        res = self.client.get(
            "api/v1/parcels",
            headers={"content-type": "application/json"}
        )
        print(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_orders_in_transit(self):
        """Return a list of orders in transit."""
        res = self.client.get(
            "/api/v1/parcels/moving",
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 200)

    def test_order_by_id(self):
        """Test get_order_by_id."""
        res = self.client.get(
            "api/v1/parcels/1", data=json.dumps(self.data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 404)

    def test_mark_parcel_as_delivered(self):
        """Test mark parcel as moving."""
        res = self.client.put(
            "api/v1/parcels/1/delivered", data=json.dumps(self.data),

            headers={"content-type": "application/json"}
        )

        self.assertEqual(json.loads(res.data)[
                         'message'], "Order not found")

    def test_declined_parcels_by_admin(self):
        """Test get declined prcels."""
        res = self.client.get(
            "api/v1/parcels/declined",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_delete_parcel(self):
        """Test delete a parcel."""
        res = self.client.delete(
            "api/v1/parcels/1", data=json.dumps(self.data),
            headers={"content-type": "application/json"}

        )
        self.assertEqual(res.status_code, 200)

    def test_get_accepted_parcels(self):
        """"Test get accepted orders."""
        res = self.client.get(
            "api/v1/parcels/delivered",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_update_status_approved(self):
        """Test update status to approved."""
        res = self.client.put(
            "api/v1/parcels/1/approved", data=json.dumps(self.data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "order not found")

    def test_completed_orders(self):
        """Test get completed orders."""
        res = self.client.get(
            "api/v1/parcels/delivered",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_non_order_by_id(self):
        """Test non_order by specific Id."""
        res = self.client.get(
            "api/v1/parcels/345",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Order not found")

    def test_non_order_delete(self):
        """Test deletion of null order ."""
        res = self.client.delete(
            "api/v1/parcels/156",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "Order not found")

    def test_declined_orders_list(self):
        """Test get declined orders."""
        res = self.client.get(
            "api/v1/parcels/declined",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_pending_order_list(self):
        """Test pending orders."""
        res = self.client.get(
            "api/v1/parcels/pending",
            headers={"content-type": "application/json"})
        self.assertEqual(res.status_code, 200)

    def test_mark_order_as_moving(self):
        """Test mark order as moving."""
        res = self.client.put(
            "api/v1/parcels/1/moving",

            headers={"content-type": "application/json"}
        )

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json.loads(res.data)[
                         'message'], "order not found")

    def test_decline_an_order(self):
        """Test admin decline order."""
        res = self.client.put(
            "api/v1/parcels/1/declined", data=json.dumps(self.data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def test_invalid_origin_name(self):
        """Test invalid origin name."""
        data = {
            "origin": "******",
            "price": 20,
            "destination": "Nairobi",
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
        """Test invalid destination."""
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
        """Test invlid price."""
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
        self.assertEqual(json.loads(res.data)['message'], {'price': 'Invalid price'})

    def test_invalid_weight(self):
        """Test invalid weight."""
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
        self.assertEqual(json.loads(res.data)['message'], {'weight': 'Invalid weight'})


if __name__ == '__main__':

    unittest.main()
