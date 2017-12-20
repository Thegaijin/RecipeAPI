# app/auth/categories.py
''' This script holds the resource functionality for category CRUD '''

# Local imports
from app import db
from app.models.category import Category
from app.models.user import User
import traceback

# Third party imports
from flask import request, jsonify
from flask_restplus import fields, Namespace, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace(
    'categories', description='Creating, viewing, editing and deleting \
    categories')

category = api.model('Category', {
    'category_name': fields.String(required=True, description='category name'),
    'description': fields.String(required=True,
                                 description='category description'),
})

# validate input
parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
parser.add_argument('category_name', required=True,
                    help='Try again: {error_msg}')
parser.add_argument('description', required=True,
                    help='Try again: {error_msg}')

# validate input
q_parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
q_parser.add_argument('q', help='search')
q_parser.add_argument('page', type=int, help='Try again: {error_msg}')
q_parser.add_argument('per_page', type=int, help='Try again: {error_msg}',
                      choices=[5, 10, 20, 30, 40, 50], default=10)


def categories(the_categories):
    user_categories = []
    if the_categories:
        for category in the_categories:
            get_response = {}
            get_response['category_id'] = category.category_id
            get_response['category_name'] = category.category_name
            get_response['description'] = category.description
            get_response['created_by'] = category.created_by

            user_categories.append(get_response)
        return user_categories


@api.route('')
class Categories(Resource):
    ''' The class handles the Category CRUD functionality '''

    @api.response(200, 'Category found successfully')
    @api.expect(q_parser)
    @jwt_required
    def get(self):
        ''' This method returns all categories

            :return: A dictionary of the category\'s properties
        '''
        args = q_parser.parse_args()
        q = args.q
        page = args.get('page', 1)
        per_page = args.get('per_page', 3)

        try:
            user_id = get_jwt_identity()
            the_categories = Category.query.filter_by(
                created_by=user_id).paginate(page=page, per_page=per_page)
            the_categories = categories(the_categories.items)
            print(the_categories)
            print(type(the_categories))
            if the_categories:
                if q:
                    # for category in the_categories.items:
                    #     if q in category.category_name:
                    #         print("the category: {}".format(category))
                    #         return categories(category)
                    the_category = [
                        category for category in the_categories if q in category.category_name]
                    print("the category: {}".format(jsonify(the_category)))
                    the_categories = jsonify({'categories': the_category})
                    print('paginated categories: {}'.format(the_categories))
            return the_categories, 200

            # return categories(the_categories)

        except Exception as e:
            get_response = {
                'message': str(e)
            }
            return get_response

        # try:
        #     if q:
        #         the_categories = Category.query.filter(
        #             Category.category_name.like(
        #                 '%' + q + '%')).paginate(page, per_page)
        #         category_list = categories(the_categories)
        #         print(category_list)

        #         for category in category_list:
        #             if q == category['category_name']:
        #                 print(category)
        #                 return category

        # except Exception as e:
        #     get_response = {
        #         'message': str(e)
        #     }

        #     return get_response, 404

    # specifies the expected input fields
    @api.expect(parser)
    @api.response(201, 'Category created successfully')
    @jwt_required
    def post(self):
        ''' This method adds a new category to the DB

        :param str name: The category name
        :param str description: The category description
        :return: A dictionary with a message
        '''
        # get current user id
        user_id = get_jwt_identity()

        args = parser.parse_args()
        category_name = args.category_name
        description = args.description
        created_by = user_id

        try:
            # check if the category exists
            if Category.query.filter_by(
                    created_by=created_by,
                    category_name=category_name).first() is None:
                category = Category(category_name, description, created_by)
                db.session.add(category)
                db.session.commit()
                the_response = {
                    'status': 'Success',
                    'message': 'Category was created',
                    'category_id': category.category_id
                }
                return the_response, 201
            return {'message': 'Category already exists'}
        except Exception as e:

            post_response = {
                'message': str(e)
            }
            traceback.print_exc()
            return post_response


@api.route('/<int:category_id>/')
class Categoryy(Resource):

    @api.response(200, 'Category found successfully')
    @jwt_required
    def get(self, category_id):
        ''' This method returns a category
        '''
        try:
            the_category = Category.query.filter_by(
                category_id=category_id).first()

            if the_category is not None:

                get_response = {}
                get_response['category_id'] = the_category.category_id
                get_response['category_name'] = the_category.category_name
                get_response['description'] = the_category.description
                get_response['created_by'] = the_category.created_by
                print(get_response)
                return get_response, 200
            # else:
            #     # get current user id
            #     username = get_jwt_identity()
            #     created_by = username
            #     the_categories = Category.query.all()

            #     return categories(the_categories)

        except Exception as e:
            get_response = {
                'message': str(e)
            }

            return get_response, 404

    @api.expect(parser)
    @api.response(204, 'Successfully edited')
    @jwt_required
    def put(self, category_id):
        ''' This method edits a category.

        :param str name: The new category name
        :param str description: The new category description
        :return: A dictionary with a message
        '''
        # get current user id
        user_id = get_jwt_identity()

        try:
            the_category = Category.query.filter_by(
                category_id=category_id).first()
            if the_category is not None:
                args = parser.parse_args()
                category_name = args.category_name
                description = args.description
                created_by = user_id

                if category_name is not None and description is not None:
                    if Category.query.filter_by(category_name=category_name,
                                                created_by=created_by).first() is None:
                        the_category.category_name = category_name
                        the_category.description = description
                        db.session.add(the_category)
                        db.session.commit()
                        edit_response = {
                            'status': 'Success',
                            'message': 'Category details successfully edited'
                        }

                        return edit_response, 204
                    return {'message': 'One or more inputs missing'}
                else:
                    return {'message': 'No changes to be made'}
                return {'message': 'The category does not exist'}
        except Exception as e:
            print('wtf')
            edit_response = {
                'message': str(e)
            }
            traceback.print_exc()
            return edit_response

    @api.response(204, 'Category was deleted')
    @jwt_required
    def delete(self, category_id):
        ''' This method deletes a Category. The method is passed the category
            name in the url and it deletes the category that matches that name.

            :param str name: The name of the category you want to delete.
            :return: A dictionary with a message confirming deletion.
        '''
        try:
            the_category = Category.query.filter_by(
                category_id=category_id).first()
            if the_category is not None:
                db.session.delete(the_category)
                db.session.commit()
                return {'message': 'Category was deleted'}
            else:
                return {'message': 'The category does not exist'}
        except Exception as e:

            post_response = {
                'message': str(e)
            }

            return post_response
