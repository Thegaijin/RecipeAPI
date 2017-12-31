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
                    help='Try again: {error_msg}')

per_page_min = 5
per_page_max = 10
# validate input
q_parser = reqparse.RequestParser(bundle_errors=True)
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
            # base_url = 'http://127.0.0.1:5000/api/v1/categories'
            # num_of_categories = len(pag_categories)

            # jsonify turns the JSON output into a Response object
            # with the application/json mimetype
            #  jsonify converts multiple arguments into an array or
            # multiple keyword arguments into a dict
            # Multiple arguments: Converted to an array before being passed to
            # dumps()
            # Multiple keyword arguments: Converted to a dict before being p
            # assed to dumps().
            return jsonify(all_categories)

        except Exception as e:
            get_response = {
                'message': str(e)
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

        try:
            # check if the category exists
            if Category.query.filter_by(
                    created_by=created_by,
                    category_name=category_name).first() is None:
                a_category = Category(category_name.lower(),
                                      description.lower(), created_by)
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
                'message': str(e)
            }

            return post_response


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
        except Exception as e:
            get_response = {
                'message': str(e)
            }

            return get_response, 404

    @api.expect(category)
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
                        the_category.category_name = category_name.lower()
                        the_category.description = description.lower()
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

            post_response = {
                'message': str(e)
            }

            return post_response
