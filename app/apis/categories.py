# app/auth/categories.py
''' This script holds the resource functionality for category CRUD '''

# Local imports
from app import db
from app.models.category import Category
from app.models.user import User
import traceback

# Third party imports
from flask import request
from flask_restplus import fields, Namespace, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace(
    'categories', description='Creating, viewing, editing and deleting \
    categories')

category = api.model('Category', {
    'name': fields.String(required=True, description='category name'),
    'description': fields.String(required=True,
                                 description='category description'),
})

# validate input
parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
parser.add_argument('name', required=True, help='Try again: {error_msg}')
parser.add_argument('description', required=True,
                    help='Try again: {error_msg}')

# validate input
q_parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
q_parser.add_argument('q', help='search')
q_parser.add_argument('page', type=int, help='Try again: {error_msg}')
q_parser.add_argument('per_page', type=int, help='Try again: {error_msg}')


def categories(the_categories):
    user_categories = []
    if the_categories:
        for category in the_categories:
            get_response = {}
            get_response['id'] = category.id
            get_response['name'] = category.name
            get_response['description'] = category.description
            get_response['created_by'] = category.created_by

            user_categories.append(get_response)
        print(user_categories)
        return user_categories, 200


@api.route('')
@api.route('/<int:id>/')
class Categories(Resource):
    ''' The class handles the Category CRUD functionality '''

    @api.response(200, 'Category found successfully')
    @api.expect(q_parser)
    @jwt_required
    def get(self, id=None):
        ''' This method returns a category or several categories depending on
            the query. In case the method is passed the category name in the
            url, it returns the details of that category.
            If no name is passed, it returns all the categories created by a
            user

            :param str name: The name of the category you want to view.
            :return: A dictionary of the category\'s properties
        '''

        try:
            if id is not None:
                the_category = Category.query.filter_by(
                    id=id).one()
                if the_category is not None:

                    get_response = {}
                    get_response['id'] = the_category.id
                    get_response['name'] = the_category.name
                    get_response['description'] = the_category.description
                    get_response['created_by'] = the_category.created_by
                    return get_response, 200
            else:
                # get current user id
                username = get_jwt_identity()
                created_by = username
                the_categories = Category.query.filter_by(
                    created_by=created_by).all()

                return categories(the_categories)

        except Exception as e:
            get_response = {
                'message': str(e)
            }

            return get_response, 404

        args = q_parser.parse_args()
        q = args['q']
        page = args['page']
        per_page = args['per_page']
        try:
            if q:
                the_categories = Category.query.filter(Category.name.like(
                    '%' + q + '%')).paginate(page, per_page)
                return categories(the_categories)

        except Exception as e:
            get_response = {
                'message': str(e)
            }

            return get_response, 404

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
        name = args.name
        description = args.description
        created_by = user_id

        try:
            # check if the category exists
            if Category.query.filter_by(name=name).first() is None:
                category = Category(name, description, created_by)
                db.session.add(category)
                db.session.commit()
                the_response = {
                    'status': 'Success',
                    'message': 'Category was created',
                    'id': category.id
                }
                return the_response, 201
            return {'message': 'Category already exists'}
        except Exception as e:

            post_response = {
                'message': str(e)
            }
            traceback.print_exc()
            return post_response

    @api.expect(parser)
    @api.response(204, 'Successfully edited')
    @jwt_required
    def put(self, id):
        ''' This method edits a category.

        :param str name: The new category name
        :param str description: The new category description
        :return: A dictionary with a message
        '''
        try:
            the_category = Category.query.filter_by(id=id).first()
            if the_category is not None:
                args = parser.parse_args()
                name = args.name
                description = args.description

                if name is not None and description is not None:
                    the_category.name = name
                    the_category.description = description
                    db.session.add(the_category)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Category details successfully edited'
                    }

                    return edit_response, 204

                else:
                    return {'message': 'No changes to be made'}
                return {'message': 'The category does not exist'}
        except Exception as e:

            edit_response = {
                'message': str(e)
            }
            traceback.print_exc()
            return edit_response

    @api.response(204, 'Category was deleted')
    @jwt_required
    def delete(self, id):
        ''' This method deletes a Category. The method is passed the category
            name in the url and it deletes the category that matches that name.

            :param str name: The name of the category you want to delete.
            :return: A dictionary with a message confirming deletion.
        '''
        try:
            the_category = Category.query.filter_by(id=id).first()
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
            traceback.print_exc()
            return post_response
