# app/auth/categories.py
''' This script holds the resource functionality for category CRUD '''

# Third party imports
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import fields, Namespace, Resource, reqparse


# Local imports
from app import db
from app.models.category import Category
from ..serializers import CategorySchema
from ..validation_helper import name_validator
from ..get_helper import per_page_max, per_page_min


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
parser.add_argument('category_name', required=True,
                    help='Try again: {error_msg}')
parser.add_argument('description', required=True,
                    help='Try again: {error_msg}', default='')


# validate input
q_parser = reqparse.RequestParser(bundle_errors=True)
# location specifies to look only in the querystring
q_parser.add_argument('q', required=False,
                      help='search for word', location='args')
q_parser.add_argument('page', required=False, type=int,
                      help='Number of pages', location='args')
q_parser.add_argument('per_page', required=False, type=int,
                      help='categories per page', default=10, location='args')


@api.route('')
class Categories(Resource):
    ''' The class handles the Category CRUD functionality '''

    @api.response(200, 'Category found successfully')
    @api.expect(q_parser)
    @jwt_required
    def get(self):
        ''' This method returns all the categories

            :return: A dictionary of the category\'s properties
        '''

        try:
            user_id = get_jwt_identity()

            # get BaseQuery object to allow for pagination
            the_categories = Category.query.filter_by(created_by=user_id)
            args = q_parser.parse_args(request)
            q = args.get('q', '')
            page = args.get('page', 1)
            per_page = args.get('per_page', 10)
            if per_page < per_page_min:
                per_page = per_page_min
            if per_page > per_page_max:
                per_page = per_page_max

            if q:
                q = q.lower()
                for a_category in the_categories.all():
                    if q in a_category.category_name.lower():
                        categoryschema = CategorySchema()
                        # dump converts python object to json object
                        the_category = categoryschema.dump(a_category)
                        # jsonify Single argument: Passed through to dumps()
                        return jsonify(the_category.data)
            pag_categories = the_categories.paginate(
                page, per_page, error_out=False)
            paginated = []
            for a_category in pag_categories.items:
                paginated.append(a_category)
            categoriesschema = CategorySchema(many=True)
            all_categories = categoriesschema.dump(paginated)
            return jsonify(all_categories)
        except Exception as e:
            get_response = {
                'View all categories exception': str(e)
            }
            return get_response

    @api.expect(category)
    @api.response(201, 'Category created successfully')
    @jwt_required
    def post(self):
        ''' This method adds a new category to the DB

        :return: A dictionary with a message and status code
        '''
        # get current user id
        user_id = get_jwt_identity()

        args = parser.parse_args()
        category_name = args.category_name
        description = args.description
        created_by = user_id

        validated_name = name_validator(category_name)
        if len(validated_name) is len(category_name):
            try:
                # change values to lowercase
                category_name = category_name.lower()
                description = description.lower()
                # check if the category exists
                if Category.query.filter_by(
                        created_by=created_by,
                        category_name=category_name).first() is None:
                    a_category = Category(category_name,
                                          description, created_by)
                    db.session.add(a_category)
                    db.session.commit()
                    the_response = {
                        'status': 'Success',
                        'message': 'Category was created',
                        'category_id': a_category.category_id
                    }
                    return the_response, 201
                return {'message': 'Category already exists'}
            except Exception as e:
                post_response = {
                    'Create Category Exception': str(e)
                }
                return post_response
        else:
            return {'Input validation Error': 'The category name should '
                    'comprise of alphabetical characters and can be more than '
                    'one word'}


@api.route('/<int:category_id>/')
class Categoryy(Resource):
    """This class handles a single category GET, PUT AND DELETE functionality
    """

    @api.response(200, 'Category found successfully')
    @jwt_required
    def get(self, category_id):
        ''' This method returns a category
        '''
        try:
            the_category = Category.query.filter_by(
                category_id=category_id).first()

            if the_category is not None:

                categoryschema = CategorySchema()
                get_response = categoryschema.dump(the_category)
                return jsonify(get_response.data)
            return {'message': 'The category doesn\'t exist'}
        except Exception as e:
            get_response = {
                'Get a category exception': str(e)
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
        user_id = get_jwt_identity()
        try:
            the_category = Category.query.filter_by(
                category_id=category_id).first()
            if the_category is not None:
                args = parser.parse_args()
                category_name = args.category_name
                description = args.description
                created_by = user_id

                # change values to lowercase
                category_name = category_name.lower()
                description = description.lower()

                # check if there's a new value is added otherwise keep previous
                if not category_name:
                    category_name = the_category.category_name
                if not description:
                    description = the_category.description

                validated_name = name_validator(category_name)
                if len(validated_name) is len(category_name):
                    # Replace old values with the new values
                    the_category.category_name = category_name
                    the_category.description = description
                    db.session.add(the_category)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Category details successfully edited'
                    }
                    return edit_response, 200

                else:
                    return {'Input validation Error': 'The category name '
                            'should comprise of alphabetical characters and '
                            'can be more than one word'}
            return {'message': 'The category does not exist'}
        except Exception as e:
            edit_response = {
                'Edit category exception': str(e)
            }
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
                return {'message': 'Category was deleted'}, 200
            return {'message': 'The category does not exist'}
        except Exception as e:

            delete_response = {
                'Delete category exception': str(e)
            }

            return delete_response
