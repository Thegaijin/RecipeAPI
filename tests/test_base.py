# base.py
''' This Script has the setup and teardown functionality '''

# Third party imports
import json
from unittest import TestCase

# Local imports
from app import create_app, db


class BaseTestCase(TestCase):
    ''' Setup the shared testing settings '''

    def setUp(self):

        # set app to use testing configuration, initialising the test_yummy db
        self.app = create_app(config_name="testing")

        # Client object to send virtual requests to the application
        self.client = self.app.test_client

        # The user details data to be used for testing
        self.user = {"username": "username", "password": "password"}
        # The Category details data to be used for testing
        self.category = {"category_name": "category",
                         "description": "description"}
        self.category1 = {"category_name": "category one",
                          "description": "description one"}
        self.recipe = {"recipe_name": "recipe",
                       "description": "description"}
        self.recipe1 = {"recipe_name": "recipe one",
                        "description": "description one"}

        # explicitly create application context
        # cache DB connections to be created on a per-request or usage case
        with self.app.app_context():
            # current_app points to app
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
