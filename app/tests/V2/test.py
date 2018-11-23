"""Tests module"""
import json
import unittest
from app import create_app
from app.db_config import destroy_tables

class BaseCase(unittest.TestCase):
    """TestCase."""
      

    def setUp(self):
        """ Fuction for setUp method."""

        self.app = create_app('testing')
        self.client = self.app.test_client()



        self.user_signup_data = {
            "email": "brian@ushcks.com",
            "password": "idfwur",
            "username": "bseremm",
            "phone" : 70027837
        }
       
        self.user_login_data = {
            "username": "hulk",
            "password": "incredible"
        }
        self.admin_login_data = {
            "username": "serem",
            "password": "andela"
        }
        self.parcel_data = {
            "name":"PS4 console",
            "origin": "Maralal",
            "destination": "Kericho",
            "weight": 12
        } 

        self.change_parcel_location_data = {
            "new location": "molo"
        }
        self.change_parcel_status_data = {
            "new status": "moving"
        }
        self.change_parcel_destination_data = {
            "destination": "molo"
        }
        
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin_login_data),
            content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        print(data)
        self.token = data['access_token']
        self.admin_header = {
            'AUTHORIZATION': 'Bearer {}'.format(self.token)
        }

        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_login_data),
            content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        print(data)
        self.token = data['access_token']
        self.user_header = {
            'AUTHORIZATION': 'Bearer {}'.format(self.token)
        }

    def test_create_user(self):
        """Test endpoint to create user"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user_signup_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        result = json.loads(response.get_data(as_text=True))
        self.assertIn('access_token', str(result))

    def test_login_admin(self):
        """Test endpoint to create user"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin_login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_signin_user(self):
        """Test endpoint to signin user"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_login_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)


    def test_create_order(self):
        """Test endpoint to create order"""
        response = self.client.post(
            '/api/v2/parcels', data=json.dumps(self.parcel_data), headers=self.admin_header, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data)
        self.assertIn('parcel created', str(result))

    def test_get_all_orders(self):
        """Test endpoint to fetch all orders"""
        self.test_create_order()
        response = self.client.get(
            '/api/v2/parcels', headers=self.admin_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('all orders', str(result))

    def test_get_specific_order(self):
        """Test endpoint to fetch a specific order"""
        response = self.client.get(
            '/api/v2/parcels/1', headers=self.admin_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('order', str(result))

    def test_get_delivery_orders_by_user(self):
        """Test endpoint to fetch delivery orders for a specific user"""
        self.test_create_order()
        response = self.client.get(
            '/api/v2/users/1/parcels', headers=self.admin_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('user', str(result))

    def test_edit_current_location(self):
        """Test endpoint to change current location"""
        self.test_create_order()
        response = self.client.put(
            '/api/v2/parcels/1/presentlocation', headers=self.admin_header, data=json.dumps(self.change_parcel_location_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('molo', str(result))

    def test_edit_parcel_destination(self):
        """Test endpoint to change current location"""
        self.test_create_order()
        response = self.client.put(
            '/api/v2/parcels/1/destination', headers=self.user_header, data=json.dumps(self.change_parcel_destination_data), content_type='application/json')
    

        result = json.loads(response.data)
        self.assertIn('owners', str(result))

    def test_edit_parcel_status(self):
        """Test endpoint to change status"""
        self.test_create_order()
        response = self.client.put(
            '/api/v2/parcels/1/status', headers=self.admin_header, data=json.dumps(self.change_parcel_status_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('moving', str(result))


    def test_create_user(self):
        """Test_create_user method."""
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.user_signup_data),
            content_type='application/json')

        self.assertEqual(res.status_code, 404)

    def test_user_not_created(self):
        """Test_user_not_found method."""
        res2 = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user_signup_data),
            content_type='application/json')
        result = json.loads(res2.data)
        self.assertEqual(res2.status_code, 404)

    def test_user_login(self):
        """Test_user_login method."""
        res2 = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_login_data),
            content_type='application/json')
        result = json.loads(res2.data)
    
        self.assertEqual(res2.status_code, 200)

    def test_create_parcel_order(self):
        """Test_create_parcel_order method."""
        res = self.client.post('/api/v2/parcels',
                               data=json.dumps(self.parcel_data),
                               content_type='application/json',
                               headers=self.admin_header)
        self.assertEqual(res.status_code, 201)

    def test_invalid_username_input(self):
        """Test_valid_username method."""
        self.data = {
            "email": "beeserem@gmail.com",
            "password": "brian",
            "username": "#####",
            "phone":700278037
        }
        res = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.data),
            content_type='application/json')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_invalid_email_input(self):
        """Test_valid_username method."""
        self.data = {
            "email": "beeserem@.com",
            "password": "brian",
            "username": "brayo",
            "phone":700278037
        }
        res = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.data),
            content_type='application/json')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
    def test_invalid_phone_input(self):
        """Test_valid_username method."""
        self.data = {
            "email": "beeserem@.com",
            "password": "brian",
            "username": "brayor",
            "phone":70027
        }
        res = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.data),
            content_type='application/json')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 400)


if __name__ == '__main__':
    unittest.main()
