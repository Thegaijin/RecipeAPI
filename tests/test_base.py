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
        self.user = {'username': 'username',
                     'password': 'password'}
        # The Category details data to be used for testing
        self.category = {'name': 'category',
                         'description': 'description'}
        # explicitly create application context
        # cache DB connections to be created on a per-request or usage case
        with self.app.app_context():
            # current_app points to app
            db.create_all()

    def tearDown(self):
        with self.app.app_context():

            db.session.close()
            db.drop_all()
