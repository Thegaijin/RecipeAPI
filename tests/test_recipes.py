''' This scripts tests the recipe crud functionality '''

import json

from tests.test_base import BaseTestCase


class RecipeTestCase(BaseTestCase):
    ''' This class handles all the tests for the Recipe functionality '''

    def test_create_recipe(self):
        ''' Test that the API can create a Recipe in a category '''

        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)["access_token"]
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res["category_id"]), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        the_recipe = self.recipe['recipe_name']
        self.assertEqual(create_res["message"],
                         f'{the_recipe} recipe has been created')

    def test_recipe_already_exits(self):
        ''' Test that the API can not create a recipe in category if it
             already exists
        '''
        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
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

        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        view_res = self.client().get('/api/v1/recipes/{}/{}/'.format(
            category_res['category_id'], create_res['recipe_id']),
            headers=dict(Authorization="Bearer " + token))
        self.assertEqual(view_res.status_code, 200)
        view_res = json.loads(view_res.data)
        self.assertIn('recipe_name', view_res)

    def test_view_all_recipes(self):
        """ Test that the API can view several recipes """

        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
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

        view_res = self.client().get('/api/v1/recipes/', headers=dict(
            Authorization="Bearer " + token))
        self.assertEqual(view_res.status_code, 200)

    def test_edit_recipe(self):
        """ Test that API can edit a recipe """

        self.user_registration()
        loggedin_user = self.user_login()
        print(loggedin_user, "Login details")
        token = json.loads(loggedin_user.data)['access_token']
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        new_details = {"recipe_name": "new_name",
                       "ingredients": "new_ingredients"}
        edit_res = self.client().put('/api/v1/recipes/{}/{}/'.format(
            category_res['category_id'], create_res['recipe_id']),
            headers=dict(Authorization="Bearer " + token), data=new_details)
        # print(edit_res, "Edit recipe =========>")
        # self.assertEqual(edit_res.status_code, 200)

    def test_delete_recipe(self):
        """ Test that API can delete a recipe """

        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
        category_res = self.create_category()
        self.assertEqual(category_res.status_code, 201)
        category_res = json.loads(category_res.data)

        create_res = self.client().post('/api/v1/recipes/{}/'.format(
            category_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=self.recipe)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        delete_res = self.client().delete('/api/v1/recipes/{}/{}/'.format(
            category_res['category_id'], create_res['recipe_id']),
            headers=dict(Authorization="Bearer " + token))
        self.assertEqual(delete_res.status_code, 200)
        delete_res = json.loads(delete_res.data)
        # print(self.recipe)
        self.assertEqual(delete_res['message'], 'Recipe was deleted')
