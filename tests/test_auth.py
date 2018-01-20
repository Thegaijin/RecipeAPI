''' This scripts handles setting up the app context for the tests '''

import json

from tests.test_base import BaseTestCase


class UserTestCase(BaseTestCase):
    ''' Tests for the user registration and login '''

    def test_user_registration(self):
        ''' Test if users are registered successfully '''

        res = self.client().post('/api/v1/auth/register/', data=self.user)
        output = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertDictEqual(
            {"message": "Account was successfully created"}, output)

    def test_user_already_exists(self):
        ''' Test that an existing username cannot be registered again '''
        res_1 = self.client().post('/api/v1/auth/register/', data=self.user)
        self.assertEqual(res_1.status_code, 201)
        res_2 = self.client().post('/api/v1/auth/register/', data=self.user)
        self.assertEqual(res_2.status_code, 409)
        output = json.loads(res_2.data)
        self.assertDictEqual(
            {'message': f"The username {self.user['username']} already exists"}, output)

    def test_user_successful_login(self):
        ''' Test if existing user can successfully login '''
        res_1 = self.client().post('/api/v1/auth/register/', data=self.user)
        self.assertEqual(res_1.status_code, 201)
        res_2 = self.client().post('/api/v1/auth/login/', data=self.user)
        self.assertEqual(res_2.status_code, 200)
        output = json.loads(res_2.data)
        self.assertEqual(output['message'], 'You have been signed in')

    def test_unregistered_user_login_fails(self):
        ''' Test if an unregistered user can sign in '''
        res = self.client().post('/api/v1/auth/login/', data=self.user)
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data)
        self.assertEqual(result['message'],
                         'Username does not exist, signup')

    def test_login_fails(self):
        ''' Test if a user can sign in with wrong credentials '''
        res_1 = self.client().post('/api/v1/auth/register/', data=self.user)
        self.assertEqual(res_1.status_code, 201)
        res_2 = self.client().post('/api/v1/auth/login/', data=self.wrong_cred)
        self.assertEqual(res_2.status_code, 401)
        result = json.loads(res_2.data)
        self.assertEqual(result['message'],
                         'Credentials do not match, try again')

    def test_valid_logout(self):
        ''' Test for logout '''
        self.user_registration()        # login user
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
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
