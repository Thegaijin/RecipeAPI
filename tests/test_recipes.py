# test_recipes.py
''' This Script has the tests for Recipe CRUD functionality '''

# Third party imports
import json

# Local import
from tests.test_base import BaseTestCase


class RecipeTestCase(BaseTestCase):
    ''' This class handles all the tests for the Recipe functionality '''

    def test_create_recipe(self):
        ''' Test that the API can create a Recipe in a category '''
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # add token to the header as part of the post request
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        self.assertEqual(create_res['message'], 'Recipe has been created')

    def test_recipe_already_exits(self):
        ''' Test that the API can not create a recipe in category if it
             already exists
        '''
        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # add token to the header as part of the post request
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        create2_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        create2_res = json.loads(create2_res.data)
        self.assertEqual(create2_res['message'], 'Recipe already exists')

    def test_view_recipe_in_category(self):
        """ Test that the API can view a recipe """

        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # add token to the header as part of the post request
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        view_res = self.client().get('/api/v1/recipes/{}/{}/'.format(
            category_res['category_id'], create_res['recipe_name']),
            headers=dict(Authorization="Bearer " + token))
        self.assertEqual(view_res.status_code, 200)
        view_res = json.loads(view_res.data)
        self.assertIn('recipe_name', view_res)

    def test_view_all_recipes(self):
        """ Test that the API can view several recipes """

        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # add token to the header as part of the post request
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        create2_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe1)

        self.assertEqual(create_res.status_code, 201)
        self.assertEqual(create2_res.status_code, 201)
        create_res = json.loads(create_res.data)
        create2_res = json.loads(create2_res.data)

        view_res = self.client().get('/api/v1/recipes', headers=dict(
            Authorization="Bearer " + token))
        self.assertEqual(view_res.status_code, 200)

    def test_edit_recipe(self):
        """ Test that API can edit a recipe """

        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # add token to the header as part of the post request
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        new_details = {'recipe_name': 'new_name',
                       'description': 'new_description'}
        edit_res = self.client().put('/api/v1/recipes/{}/{}/'.format(
            category_res['category_id'], create_res['recipe_name']),
            headers=dict(Authorization="Bearer " + token), data=new_details)
        self.assertEqual(edit_res.status_code, 200)

    def test_delete_recipe(self):
        """ Test that API can delete a recipe """

        # register user
        self.user_registration()
        # login user
        loggedin_user = self.user_login()
        # get token from login response object
        token = json.loads(loggedin_user.data)['access_token']
        # add token to the header as part of the post request
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        delete_res = self.client().delete('/api/v1/recipes/{}/{}/'.format(
            category_res['category_id'], create_res['recipe_name']),
            headers=dict(Authorization="Bearer " + token))
        self.assertEqual(delete_res.status_code, 200)
        delete_res = json.loads(delete_res.data)
        self.assertEqual(delete_res['message'], 'Recipe was deleted')
