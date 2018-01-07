# test_recipes.py
''' This Script has the tests for Category CRUD functionality '''

# Third party imports
import json


# Local import
from tests.test_base import BaseTestCase


class CategoryTestCase(BaseTestCase):
    ''' Tests for Category and recipe CRUD '''

    def test_create_category(self):
        ''' Test that the API can create a Category '''
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # add token to the header as part of the post request
        create_res = self.client().post('/api/v1/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)

        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)

        self.assertEqual(create_res['message'], 'Category was created')
        # self.assertIsNotNone(Category.query.filter_by(name='newname').first())

    def test_category_already_exists(self):
        ''' Test that the API can not create a Category that already exists '''
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # add token to the header as part of the post request
        create_res = self.client().post('/api/v1/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)
        create2_res = self.client().post('/api/v1/categories',
                                         headers=dict(
                                             Authorization="Bearer " + token),
                                         data=self.category)

        create2_res = json.loads(create2_res.data)
        self.assertEqual(create2_res['message'], 'Category already exists')

    def test_view_category(self):
        ''' Test that the API can view a category '''
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # create category
        create_res = self.client().post('/api/v1/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)

        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        # check for category
        view_res = self.client().get('/api/v1/categories/{}/'.format(
            create_res['category_id']), headers=dict(
                Authorization="Bearer " + token))

        self.assertEqual(view_res.status_code, 200)
        view_res = json.loads(view_res.data)
        self.assertEqual(view_res['category_name'], 'category')
        # self.assertIn(view_res, 'category')
        # self.assertIsNotNone(Category.query.filter_by(name='newname').first())

    def test_view_all_categories(self):
        ''' Test that the API can view all categories '''
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # create category
        create_res = self.client().post('/api/v1/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)

        create2_res = self.client().post('/api/v1/categories',
                                         headers=dict(
                                             Authorization="Bearer " + token),
                                         data=self.category1)
        self.assertEqual(create_res.status_code, 201)
        self.assertEqual(create2_res.status_code, 201)
        create_res = json.loads(create_res.data)
        create2_res = json.loads(create2_res.data)

        # check for category
        view_res = self.client().get('/api/v1/categories',
                                     headers=dict(
                                         Authorization="Bearer " + token))
        self.assertEqual(view_res.status_code, 200)
        self.assertIn(b'category', view_res.data)

    def test_edit_category(self):
        ''' Test that the API can view all categories '''
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # create category
        create_res = self.client().post('/api/v1/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        new_details = {'category_name': 'new_name',
                       'description': 'new_description'}
        edit_res = self.client().put('/api/v1/categories/{}/'.format(
            create_res['category_id']), headers=dict(
                Authorization="Bearer " + token),
            data=new_details)
        self.assertEqual(edit_res.status_code, 200)

    def test_delete_category(self):
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # create category
        create_res = self.client().post('/api/v1/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        delete_res = self.client().delete(
            '/api/v1/categories/{}/'.format(
                create_res['category_id']), headers=dict(
                    Authorization="Bearer " + token))
        self.assertEqual(delete_res.status_code, 200)
        delete_res = json.loads(delete_res.data)
        self.assertEqual(delete_res['message'], 'Category was deleted')
        # self.assertIsNone(Category.query.filter_by(name='category').first())
