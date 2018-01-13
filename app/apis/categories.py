from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import fields, Namespace, Resource, reqparse

from app import db
from app.models.category import Category
from ..serializers import CategorySchema
from ..validation_helper import name_validator
from ..get_helper import PER_PAGE_MAX, PER_PAGE_MIN


api = Namespace(
    'categories', description='Creating, viewing, editing and deleting \
    categories')

category = api.model('Category', {
    'category_name': fields.String(required=True, description='category name'),
    'description': fields.String(required=True,
                                 description='category description')
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


@api.route('/')
class Categories(Resource):
    ''' The class handles the Category CRUD functionality '''

    @api.response(200, 'Category found successfully')
    @api.expect(q_parser)
    @jwt_required
    def get(self):
        ''' This method returns all the categories

            :return: A dictionary of the category\'s properties
        '''
        user_id = get_jwt_identity()

        # get BaseQuery object to allow for pagination
        the_categories = Category.query.filter_by(created_by=user_id)
        args = q_parser.parse_args(request)
        q = args.get('q', '')
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        if per_page < PER_PAGE_MIN:
            per_page = PER_PAGE_MIN
        if per_page > PER_PAGE_MAX:
            per_page = PER_PAGE_MAX

        if q:
            q = q.lower()
            the_categories = Category.query.filter(
                Category.category_name.like("%" + q + "%"))
            for a_category in the_categories.all():
                if q in a_category.category_name.lower():
                    categoryschema = CategorySchema()
                    the_category = categoryschema.dump(a_category)
                    return jsonify(the_category.data)
        pag_categories = the_categories.paginate(
            page, per_page, error_out=False)
        paginated = []
        for a_category in pag_categories.items:
            paginated.append(a_category)
        categoriesschema = CategorySchema(many=True)
        all_categories = categoriesschema.dump(paginated)
        return jsonify(all_categories)

    @api.expect(category)
    @api.response(201, 'Category created successfully')
    @jwt_required
    def post(self):
        ''' This method adds a new category to the DB

        :return: A dictionary with a message and status code
        '''
        user_id = get_jwt_identity()

        args = parser.parse_args()
        category_name = args.category_name
        description = args.description
        created_by = user_id

        validated_name = name_validator(category_name)
        if validated_name:
            category_name = category_name.lower()
            description = description.lower()

            if Category.query.filter_by(
                    created_by=created_by,
                    category_name=category_name).first() is not None:
                return {'message': 'Category already exists'}, 409
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
        return {'message': 'The category name should comprise of alphabetical '
                'characters and can be more than one word'}, 400


@api.route('/<int:category_id>/')
class Categoryy(Resource):
    ''' This class handles a single category GET, PUT AND DELETE functionality
    '''

    @api.response(200, 'Category found successfully')
    @jwt_required
    def get(self, category_id):
        ''' This method returns a category '''
        the_category = Category.query.filter_by(
            category_id=category_id).first()

        if the_category is None:
            return {'message': 'The category doesn\'t exist'}, 404
        categoryschema = CategorySchema()
        get_response = categoryschema.dump(the_category)
        return jsonify(get_response.data)

    @api.expect(parser)
    @api.response(204, 'Successfully edited')
    @jwt_required
    def put(self, category_id):
        ''' This method edits a category.

        :param str name: The new category name
        :param str description: The new category description
        :return: A dictionary with a message
        '''
        args = parser.parse_args()
        category_name = args.category_name
        description = args.description

        category_name = category_name.lower()
        description = description.lower()
        the_category = Category.query.filter_by(
            category_id=category_id).first()
        if the_category is None:
            return {'message': 'The category does not exist'}

        if not category_name:
            category_name = the_category.category_name
        if not description:
            description = the_category.description

        validated_name = name_validator(category_name)
        if validated_name:
            the_category.category_name = category_name
            the_category.description = description
            db.session.add(the_category)
            db.session.commit()
            response = {
                'status': 'Success',
                'message': 'Category details successfully edited'
            }
            return response, 200
        return {'Input validation Error': 'The category name should comprise '
                'of alphabetical characters and can be more than one word'}

    @api.response(204, 'Category was deleted')
    @jwt_required
    def delete(self, category_id):
        ''' This method deletes a Category. The method is passed the category
            name in the url and it deletes the category that matches that name.

            :param str category_id: The id of the category you want to delete.
            :return: A dictionary with a message confirming deletion.
        '''

        the_category = Category.query.filter_by(
            category_id=category_id).first()
        if the_category is not None:
            db.session.delete(the_category)
            db.session.commit()
            return {'message': 'Category was deleted'}, 200
        return {'message': 'The category does not exist'}
