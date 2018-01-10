# test_recipes.py
''' This Script has the tests for user registration and login functionality '''

# Third party imports
import json
from unittest import TestCase

# Local import
from tests.test_base import BaseTestCase


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
            {"message": "Account was successfully created"}, output)

    def test_user_already_exists(self):
        ''' Test that an existing username cannot be registered again '''
        # attempt to register user 1
        res_1 = self.client().post('/api/v1/auth/register/', data=self.user)
        # check response
        self.assertEqual(res_1.status_code, 201)
        # attempt to register user 2 with the same details as user 1
        res_2 = self.client().post('/api/v1/auth/register/', data=self.user)
        # check response
        self.assertEqual(res_2.status_code, 409)
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
        self.assertEqual(result['Login error'],
                         'Username does not exist, signup')

    def test_login_fails(self):
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
        self.assertEqual(result['Login error'],
                         'Credentials do not match, try again')

    def test_valid_logout(self):
        ''' Test for logout '''
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # valid token logout
        delete_res = self.client().delete('/api/v1/auth/logout/', headers=dict(
            Authorization="Bearer " + token))
        self.assertEqual(delete_res.status_code, 200)
        delete_res = json.loads(delete_res.data)
        self.assertEqual(delete_res['message'], 'Successfully logged out')

    def test_reset_password(self):
        ''' Test reset password '''
        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
        passwords = {"old_password": "password",
                     "new_password": "new_password"}
        reset_res = self.client().put('/api/v1/auth/reset_password/',
                                      headers=dict(
                                          Authorization="Bearer " + token,
                                          data=passwords))
        self.assertEqual(reset_res.status_code, 200)
