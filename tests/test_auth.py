# test_recipes.py
''' This Script has the tests for the application functionality '''

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

        # The user details json data to be used for testing
        self.user = {'username': 'username',
                     'password': 'password'}

        # explicitly create application context
        # cache DB connections to be created on a per-request or usage case
        with self.app.app_context():
            # current_app points to app
            db.create_all()

    def tearDown(self):
        with self.app.app_context():

            db.session.close()
            db.drop_all()


class UserTestCase(BaseTestCase):
    ''' Tests for the user registration and login '''

    def test_user_registration(self):
        ''' Test if users are registered successfully '''
        # register user

        res = self.client().post('/api/v1/auth/register/', data=self.user)
        # pick the data in json format
        output = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 201)
        self.assertDictEqual(
            {'message': 'Account was successfully created'}, output)

    def test_user_already_exists(self):
        ''' Test that an existing username cannot be registered again '''
        # attempt to register user 1
        res_1 = self.client().post('/api/v1/auth/register/', data=self.user)
        # check response
        self.assertEqual(res_1.status_code, 201)
        # attempt to register user 2 with the same details as user 1
        res_2 = self.client().post('/api/v1/auth/register/', data=self.user)
        # check response
        self.assertEqual(res_2.status_code, 202)
        # get the results returned in json format
        output = json.loads(res_2.data)
        self.assertDictEqual(
            {'message': "The username already exists"}, output)

    def test_user_successful_login(self):
        ''' Test if existing user can successfully login '''
        # attempt to register user
        res_1 = self.client().post('/api/v1/auth/register/', data=self.user)
        # check response
        self.assertEqual(res_1.status_code, 201)
        # attempt to login user
        res_2 = self.client().post('/api/v1/auth/login/', data=self.user)
        # check response
        self.assertEqual(res_2.status_code, 200)
        output = json.loads(res_2.data)
        self.assertEqual(output['message'], 'You have been signed in')

    def test_unregistered_user_login_fails(self):
        ''' Test if an unregistered user can sign in '''
        # attempt to login user
        res = self.client().post('/api/v1/auth/login/', data=self.user)
        # check response
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data)
        self.assertEqual(result['message'], 'Username does not exist, signup')

    def test_user_wrong_credentials_login_fails(self):
        ''' Test if a user can sign in with wrong credentials '''
        # attempt to register user
        res_1 = self.client().post('/api/v1/auth/register/', data=self.user)
        # check response
        self.assertEqual(res_1.status_code, 201)
        self.wrong_cred = {'username': 'username',
                           'password': '12345'}
        res_2 = self.client().post('/api/v1/auth/login/', data=self.wrong_cred)
        # check response
        self.assertEqual(res_2.status_code, 401)
        result = json.loads(res_2.data)
        self.assertEqual(result['message'],
                         'Credentials do not match, try again')
