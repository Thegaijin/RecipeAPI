''' This scripts tests the category crud functionality '''

import json

from tests.test_base import BaseTestCase


class CategoryTestCase(BaseTestCase):
    ''' Tests for Category and recipe CRUD '''

    def test_create_category(self):
        ''' Test that the API can create a Category '''
        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
        create_res = self.client().post('/api/v1/categories/',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)

        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        the_category = self.category['category_name']
        self.assertEqual(
            create_res['message'], f'{the_category} category was created')

    def test_category_already_exists(self):
        ''' Test that the API can not create a Category that already exists '''
        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
        create_res = self.client().post('/api/v1/categories/',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)
        create2_res = self.client().post('/api/v1/categories/',
                                         headers=dict(
                                             Authorization="Bearer " + token),
                                         data=self.category)

        create2_res = json.loads(create2_res.data)
        self.assertEqual(create2_res['message'], 'Category already exists')

    def test_view_category(self):
        ''' Test that the API can view a category '''
        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
        create_res = self.client().post('/api/v1/categories/',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)

        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        view_res = self.client().get('/api/v1/categories/{}/'.format(
            create_res['category_id']), headers=dict(
                Authorization="Bearer " + token))

        self.assertEqual(view_res.status_code, 200)
        view_res = json.loads(view_res.data)
        self.assertEqual(view_res['category_name'], 'category')

    def test_view_all_categories(self):
        ''' Test that the API can view all categories '''
        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
        create_res = self.client().post('/api/v1/categories/',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)

        create2_res = self.client().post('/api/v1/categories/',
                                         headers=dict(
                                             Authorization="Bearer " + token),
                                         data=self.category1)
        self.assertEqual(create_res.status_code, 201)
        self.assertEqual(create2_res.status_code, 201)
        create_res = json.loads(create_res.data)
        create2_res = json.loads(create2_res.data)
        view_res = self.client().get('/api/v1/categories/',
                                     headers=dict(
                                         Authorization="Bearer " + token))
        self.assertEqual(view_res.status_code, 200)
        self.assertIn(b'category', view_res.data)

    def test_edit_category(self):
        ''' Test that the API can view all categories '''
        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
        create_res = self.client().post('/api/v1/categories/',
                                        headers=dict(
                                            Authorization="Bearer " + token),
                                        data=self.category)
        self.assertEqual(create_res.status_code, 201)
        create_res = json.loads(create_res.data)
        new_details = {"category_name": "new_name",
                       "description": "new_description"}
        edit_res = self.client().put('/api/v1/categories/{}/'.format(
            create_res['category_id']), headers=dict(
                Authorization="Bearer " + token), data=new_details)
        self.assertEqual(edit_res.status_code, 200)

    def test_delete_category(self):
        ''' Test that API can delete a category '''
        self.user_registration()
        loggedin_user = self.user_login()
        token = json.loads(loggedin_user.data)['access_token']
        create_res = self.client().post('/api/v1/categories/',
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
