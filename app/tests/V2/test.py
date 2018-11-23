"""Tests module"""
import json
import unittest
from app import create_app

class BaseCase(unittest.TestCase):
    """docstring for TestCase."""

    def setUp(self):
        """Docstring for setUp method."""
        self.app = create_app('testing')
        self.client = self.app.test_client()


        self.signup_to_create_parcel_order = {
            "email": "bran@ushcks.com",
            "password": "brian",
            "username": "brian",
            "phone" : 70027837}

        self.signup_data = {
            "email": "bran@ushcks.com",
            "password": "brian",
            "username": "brian",
            "phone" : 70027837
        }
       
        self.login_data = {
            "username": "brian",
            "password": "brian"
        }
        self.login_admin = {
            "username": "serem",
            "password": "andela"
        }
        self.parcel_data = {
            "name":"PS4 console",
            "origin": "Marlala",
            "destination": "Kericho",
            "weight": 12
        }
        self.specific_data = {
             "name":"PS4 console",
            "origin": "Marlala",
            "destination": "Kericho",
            "weight": 12
        }

        
        self.user_data = {
            "username": "brian",
            "email": "bee@gmail.com",
            "password": "Ac67789"
        }

        

        
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.signup_data),
            content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.login_data),
            content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.token = data.get('access_token')
        self.user_headers = {
            'AUTHORIZATION': 'Bearer {}'.format(self.token)
        }
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.signup_admin),
            content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.login_admin),
            content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.token = data.get('access_token')
        self.admin_headers = {
            'AUTHORIZATION': 'Bearer ' + self.token
        }


        self.headers = {}

    def test_create_user(self):
        """Test endpoint to create user"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        result = json.loads(response.data)
        self.assertIn('Signup successul!', str(result))

    def test_create_admin(self):
        """Test endpoint to create user"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.admin_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data)
        self.assertIn('Signup successul!', str(result))

    def test_signin_user(self):
        """Test endpoint to signin user"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user_data), content_type='application/json')
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        result = json.loads(response.data)
        self.assertIn('access', str(result))

    def test_create_order(self):
        """Test endpoint to create order"""
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.user_data),
                      content_type='application/json')
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')

        result = json.loads(response.data)

        req_header = {'Authorization': 'Bearer {}'.format(result.get('access_token'))}
        response = self.client.post(
            '/api/v2/parcels', data=json.dumps(self.order_data), headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data)
        self.assertIn('pending', str(result))

        self.client.post('/api/v2/auth/signup', data=json.dumps(self.admin_data),
                      content_type='application/json')

        new_order = self.order_data
        new_order['pick up location'] = ""

        response = self.client.post(
            '/api/v2/parcels', data=json.dumps(new_order), headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        result = json.loads(response.data)
        self.assertIn('Error', str(result))

    def test_get_all_orders(self):
        """Test endpoint to fetch all orders"""
        self.test_create_order()
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result.get('access_token'))}
        response = self.client.get(
            '/api/v2/parcels', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('order_no', str(result))

    def test_get_specific_order(self):
        """Test endpoint to fetch a specific order"""
        self.test_create_order()
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.client.get(
            '/api/v2/parcels/1', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('order_no', str(result))

    def test_get_delivery_orders_by_user(self):
        """Test endpoint to fetch delivery orders for a specific user"""
        self.test_create_order()
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.client.get(
            '/api/v2/users/1/parcels', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('Delivery orders list', str(result))

    def test_cancel_delivery_order(self):
        """Test endpoint to cancel delivery order"""
        self.test_create_order()
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result.get('access_token'))}
        response = self.client.put(
            '/api/v2/parcels/1/cancel', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('canceled', str(result))

    def test_edit_current_location(self):
        """Test endpoint to change current location"""
        self.test_create_order()
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result.get('access_token'))}
        response = self.client.put(
            '/api/v2/parcels/1/presentLocation', headers=req_header, data=json.dumps(self.edit_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('kikuyu', str(result))

    def test_edit_status(self):
        """Test endpoint to change status"""
        self.test_create_order()
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result.get('access_token'))}
        response = self.client.put(
            '/api/v2/parcels/1/status', headers=req_header, data=json.dumps(self.edit_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('in transit', str(result))

    def test_change_delivery_location(self):
        """Test endpoint to change delivery location"""
        self.test_create_order()
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result.get('access_token'))}
        response = self.client.put(
            '/api/v2/parcels/1/destination', headers=req_header, data=json.dumps(self.edit_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('narok', str(result))

    def test_get_delivered_orders_for_user(self):
        """Test endpoint to get the number of delivered orders for a specific user"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.admin_data), content_type='application/json')
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result.get('access_token'))}
        response = self.client.get(
            '/api/v2/users/1/delivered', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('Delivered', str(result))

    def test_get_in_transit_orders_for_user(self):
        """Test endpoint to get the number of orders in transit for a specific user"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.admin_data), content_type='application/json')
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result.get('access_token'))}
        response = self.client.get(
            '/api/v2/users/1/in-transit', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('in-transit', str(result))

    def test_create_user(self):
        """Docstring for test_create_user method."""
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.signup_to_create_parcel_order),
            content_type='application/json')

        self.assertEqual(res.status_code, 201)

    def test_user_not_created(self):
        """Docstring for test_user_not_found method."""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.signup_data),
            content_type='application/json')
        res2 = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.signup_data),
            content_type='application/json')
        result = json.loads(res2.data)
        self.assertEqual(result["message"], "user already exists")
        self.assertEqual(res2.status_code, 409)

    def test_user_login(self):
        """Docstring for test_user_login method."""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.signup_data),
            content_type='application/json')
        res2 = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.login_data),
            content_type='application/json')
        result = json.loads(res2.data)
        self.assertEqual(result['message'], "successful login")
        self.assertEqual(res2.status_code, 200)

    def test_create_parcel_order(self):
        """Docstring for test_create_parcel_order method."""
        res = self.client.post('/api/v2/parcels',
                               data=json.dumps(self.parcel_data),
                               content_type='application/json',
                               headers=self.user_headers)
        self.assertEqual(res.status_code, 201)

    def test_valid_username_input(self):
        """Docstring for test_valid_username method."""
        self.data = {
            "email": "beeserem@gmail.com",
            "password": "brian",
            "username": "#####"
        }
        res = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.data),
            content_type='application/json')
        result = json.loads(res.data)
        self.assertEqual(result['message'], "your username should contain letters and numbers only")
        self.assertEqual(res.status_code, 400)



if __name__ == '__main__':
    unittest.main()
