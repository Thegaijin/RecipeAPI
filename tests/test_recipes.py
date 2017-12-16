# test_recipes.py
''' This Script has the tests for CRUD functionality '''

# Third party imports
import json
from unittest import TestCase

# Local import
from tests.test_base import BaseTestCase
from app.models.category import Category


class RecipeTestCase(BaseTestCase):
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
        create_res = self.client().post('/api/v1/recipes/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)
        # print('*****************************$$$******************************')
        # print(create_res.data)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)

        self.assertEqual(create_res['message'], 'Category was created')
        # self.assertIsNotNone(Category.query.filter_by(name='newname').first())

    def test_category_already_exists(self):
        ''' Test that the API can create a Category '''
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # add token to the header as part of the post request
        create_res = self.client().post('/api/v1/recipes/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)
        create2_res = self.client().post('/api/v1/recipes/categories',
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
        print('**************************************************************')
        # create category
        create_res = self.client().post('/api/v1/recipes/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)

        # print(create_res.data)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        # print(create_res)
        # check for category
        view_res = self.client().get('/api/v1/recipes/categories/{}/'.format(
            create_res['id']), headers=dict(Authorization="Bearer " + token))

        self.assertEqual(view_res.status_code, 200)
        view_res = json.loads(view_res.data)
        print("loads: {}".format(view_res))
        self.assertEqual(view_res['name'], 'category')
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
        # print('**************************************************************')
        # create category
        create_res = self.client().post('/api/v1/recipes/categories',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)
        print(create_res)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        print("loads: {}".format(create_res))
        print(create_res.data)
        # check for category
        view_res = self.client().get('/api/v1/recipes/categories',
                                     headers=dict(Authorization="Bearer " + token))

        self.assertEqual(view_res.status_code, 200)
        view_res = json.loads(view_res.data)
        print("loads: {}".format(view_res))
        self.assertEqual(view_res['message'], 'The category exists')
        self.assertIn(view_res.data, 'category')

    # def test_edit_category(self):
    #     ''' Test that the API can view all categories '''
    #     # register user
    #     self.user_registration()
    #     # login user
    #     loggedin_user = self.user_login()
    #     # get token from login response object
    #     token = json.loads(loggedin_user.data)['access_token']
    #     # create category
    #     create_res = self.client().post('/api/v1/recipes/categories',
    #                                     headers=dict(
    #                                         Authorization="Bearer " + token),
    #                                     data=self.category)
    #     self.assertEqual(create_res.status_code, 201)
    #     new_details = {'name': 'new_name',
    #                    'description': 'new_description'}
    #     edit_res = self.client().put('/api/v1/recipes/categories/{}/'.format(
    #         create_res['id']), headers=dict(Authorization="Bearer " + token),
    #         data=new_details)
    #     self.assertEqual(edit_res.status_code, 200)
    #     self.assertEqual(edit_res['message'], 'Category edit was successful')
    #     self.assertIn(edit_res, 'new_name')
    #     self.assertIsNotNone(Category.query.filter_by(name='newname').first())

    # def test_delete_category(self):
    #     # register user
    #     self.user_registration()
    #     # login user
    #     loggedin_user = self.user_login()
    #     # get token from login response object
    #     token = json.loads(loggedin_user.data)['access_token']
    #     # create category
    #     create_res = self.client().post('/api/v1/recipes/categories',
    #                                     headers=dict(
    #                                         Authorization="Bearer " + token),
    #                                     data=self.category)
    #     self.assertEqual(create_res.status_code, 201)
    #     delete_res = self.client().delete(
    #         '/api/v1/recipes/categories/{}/'.format(
    #             create_res['id']), headers=dict(Authorization="Bearer " + token))
    #     self.assertEqual(delete_res.status_code, 200)
    #     self.assertEqual(delete_res['message'], 'Category was deleted')
    #     self.assertIsNone(Category.query.filter_by(name='category').first())
