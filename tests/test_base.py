''' This script holds the universal configurations of the test cases '''

import json
from unittest import TestCase

from app import create_app, db


class BaseTestCase(TestCase):
    ''' Setup the shared testing settings '''

    def setUp(self):

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        self.user = {"username": "username",
                     "password": "password", "email": "email@email.com"}
        self.category = {"category_name": "category",
                         "description": "description"}
        self.category1 = {"category_name": "category one",
                          "description": "description one"}
        self.recipe = {"recipe_name": "recipe",
                       "ingredients": "description"}
        self.recipe1 = {"recipe_name": "recipe one",
                        "ingredients": "description one"}
        self.wrong_cred = {'username': 'username',
                           'password': '12345'}

        with self.app.app_context():
            db.create_all()

    def user_registration(self):
        ''' This method registers a user '''

        return self.client().post('/api/v1/auth/register/', data=self.user)

    def user_login(self):
        ''' This helper method helps log in a test user '''

        return self.client().post('/api/v1/auth/login/', data=self.user)

    def create_category(self):
        ''' This method creates a category to be used for recipe tests '''
        login = self.user_login()
        token = json.loads(login.data)['access_token']
        return self.client().post('/api/v1/categories/',
                                  headers=dict(
                                      Authorization="Bearer " + token),
                                  data=self.category)

    def tearDown(self):
        with self.app.app_context():

            db.session.close()
            db.drop_all()
