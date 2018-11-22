"""Contain test cases for the endpoints."""
import unittest
import json
from app.db_config import create_orders_table,create_users_table, create_super_admin
from app import create_app


class BaseTest(unittest.TestCase):
    def setUp(self):
        """ setting up testing """

        self.app = create_app('testing')
        self.client = self.app.test_client()
        create_orders_table()
        create_super_admin()
        create_users_table()

        self.correct_user_signup_data = {
            "username": "myname",
            "email": "myname@domain.com",
            "password": "haysbd"
        }
        self.correct_user_login_data = {
            "username": "myname",
            "password": "haysbd"
        }
        self.correct_admin_login_data = {
            "username": "brian",
            "password": "andela"
        }
        self.correct_post_parcel_data = {
            "destiantion": "nakuru",
            "weight": 56,
            "origin":"nairobi"
        }
        self.incorrect_post_parcel_data = {
            "origin": "kisii",
            "destination": "*????",
            "weight": 25
        }
        self.incorrect_origin_name = {
            "origin": "***********1",
            "destination": "Mombasa",
            "weight":20 
        }

        self.incorrect_pass_data = {
            "username": "miau",
            "password": "mooo"
        }
        self.email_already_exists_data = {
            "username": "myname",
            "email": "myname@mydomain.com",
            "password": "haysbd"
        }
        self.existing_username_data = {
            "username": "myname",
            "email": "myname@mydomain.com",
            "password": "haysbd"
        }

        

   
    def signup(self):
        """ user signup function """
        response = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(self.correct_user_signup_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login(self):
        """ login function """
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(self.correct_user_login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login_admin(self):
        """ method to login admin """
        response = self.client.post(
            "api/v2/auth/login",
            data=json.dumps(self.correct_admin_login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def get_token_as_user(self):
        """get token """
        self.signup()
        response = self.login()
        token = json.loads(response.data).get("token", None)
        return token

    def get_token_as_admin(self):
        """get token """
        response = self.login_admin()
        token = json.loads(response.data).get("token", None)
        return token

    def update_destination(self):
        '''update destination'''

        token = self.get_token_as_user()

        
        res = self.client.put(
            "api/v2/parcels/1/destination",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        
        return res


    def post_parcel(self):
        """ method to post new food item """

        token = self.get_token_as_user()

        res = self.client.post(
            "/api/v2/parcels",
            data=json.dumps(self.correct_post_parcel_data),
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        return res


class TestPostParcel(BaseTest):

    def test_post_parcel(self):
        ''' test for  posting a parcel'''
        response = self.post_parcel()

        self.assertEqual(response.status_code, 201)

    def test_get_parcel_order_does_not_exist(self):
        """ Test parcel order does not exist """
        token = self.get_token_as_user()

        response = self.client.get(
            "api/v2/parcels/100",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)

    def test_accept_order(self):
        """ test to accept order """

        token = self.get_token_as_admin()

        self.post_parcel()

        response = self.accept_order()
        print(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)[
            'message'], "your order has been approved")

        self.assertEqual(response.status_code, 200)
    
    def test_get_one_order(self):
        """test for get one one order"""

        token = self.get_token_as_user()

        self.post_parcel()

        response = self.client.get(
            "api/v2/parcels/1",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)
    
    def test_get_one_order_non_exist(self):
        """tes for orders non exsitent orders"""

        token = self.get_token_as_user()

        self.post_parcel()

        response = self.client.get(
            "api/v2/parcels/100000",
             headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 404)
    

    def test_admin_update_location(self):

        token = self.get_token_as_admin()

        self.post_parcel()
        self.accept_order()
        
        res = self.client.put(
            "/api/v2/parcels/1/presentlocation",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'})

        self.assertEqual(res.status_code,200)

    def test_get_specific_user_orders(self):

        token = self.get_token_as_user()
        self.post_parcel()
        response = self.client.get(
            "/api/v2/users/2/parcels",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_specific_user_orders_user_not_existing(self):

        token = self.get_token_as_admin()

        response = self.client.get(
            "/api/v2/users/1000000/parcels",
            headers={'content-type': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 404)
    
   
        


if __name__ == '__main__':

    unittest.main()
