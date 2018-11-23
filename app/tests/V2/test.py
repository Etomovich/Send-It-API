"""  for v2 __init__.py."""
import json
import unittest
from app import create_app
from app.db_config import destroy_tables


class BaseCase(unittest.TestCase):
    """  for TestCase."""

    def setUp(self):
        """  for setUp method."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.signup_to_create_parcel_order = {
            "email": "serem@gmail.com",
            "username": "serem",
            "password": "data",
            "phone": 700278037
        }

        self.signup_data = {
            "email": "serem@gmail.com",
            "username": "serem",
            "password": "data",
            "phone": 700278037
        }
        self.login_admin = {
            "username": "serem",
            "password": "andela",
            
        }
        self.login_data = {
            "username": "serem",
            "password": "data"
        }
        
        self.parcel_data = {
            "name": "PS4 console",
            "origin": "Nairobi",
            "destination": "Maralal",
            "weight": 12
        }
        self.specific_data = {
            "name": "PS4 console",
            "origin": "Nairobi",
            "destination": "Maralal",
            "weight": 78
        }
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.signup_data),
            content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.login_data),
            content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.token = data['access_token']
        self.user_headers = {
            'Authorization':'Bearer {}'.format(self.token)}
        
        self.client.post()
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.login_admin),
            content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.token = data['access_token']
        self.admin_headers = {
            'AUTHORIZATION': 'Bearer {}'.format(self.token)
        }

    def tearDown(self):
        """  for tearDown method."""
        destroy_tables()

class UserViewsCase(BaseCase):
    """  for TestCase."""

    def test_create_user(self):
        """  for test_create_user method."""
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.signup_to_create_parcel_order),
            content_type='application/json')

        self.assertEqual(res.status_code, 201)

    def test_user_not_created(self):
        """  for test_user_not_found method."""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.signup_data),
            content_type='application/json')
        res2 = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.signup_data),
            content_type='application/json')
        result = json.loads(res2.data)
        self.assertEqual(result['message'], "user already exists")
        self.assertEqual(res2.status_code, 409)

    def test_user_login(self):
        """  for test_user_login method."""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.signup_data),
            content_type='application/json')
        res2 = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.login_data),
            content_type='application/json')
        result = json.loads(res2.data)
    
        self.assertEqual(res2.status_code, 200)

    def test_create_parcel_order(self):
        """  for test_create_parcel_order method."""
        res = self.client.post('/api/v2/parcels',
                               data=json.dumps(self.parcel_data),
                               content_type='application/json',
                               headers=self.user_headers)
        self.assertEqual(res.status_code, 201)

    def test_valid_username_input(self):
        """ for test_valid_username method."""
        self.data = {
            "email": "serem@gmail.com",
            "username": "serem",
            "password": "data",
            "phone": 700278037
        }
        res = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.data),
            content_type='application/json')
        result = json.loads(res.data)
        self.assertEqual(result['message'], "Please enter a valid username")
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':

    unittest.main()
