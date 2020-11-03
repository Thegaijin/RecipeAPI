''' This script handles the categories CRUD '''

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import fields, Namespace, Resource, reqparse
from sqlalchemy import func

from app import db
from app.models.category import Category
from ..serializers import CategorySchema
from ..validation_helper import name_validator
from ..get_helper import PER_PAGE_MAX, PER_PAGE_MIN


api = Namespace(
    'categories', description='Creating, viewing, editing and deleting \
    categories')

CATEGORY = api.model('Category', {
    'category_name': fields.String(required=True, description='category name'),
    'description': fields.String(required=True,
                                 description='category description')
})

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('category_name', required=True,
                    help='Try again: {error_msg}')
PARSER.add_argument('description', required=True,
                    help='Try again: {error_msg}', default='')

EDIT_PARSER = reqparse.RequestParser(bundle_errors=True)
EDIT_PARSER.add_argument('category_name', required=False,
                         help='Try again: {error_msg}')
EDIT_PARSER.add_argument('description', required=False,
                         help='Try again: {error_msg}', default='')

Q_PARSER = reqparse.RequestParser(bundle_errors=True)
Q_PARSER.add_argument('q', required=False,
                      help='search for word', location='args')
Q_PARSER.add_argument('page', required=False, type=int,
                      help='Number of pages', location='args')
Q_PARSER.add_argument('per_page', required=False, type=int,
                      help='categories per page', default=10, location='args')


@api.route('/')
class Categories(Resource):
    ''' The class handles the Category CRUD functionality '''

    @api.response(200, 'Category found successfully')
    @api.expect(Q_PARSER)
    @jwt_required
    def get(self):
        ''' This method returns all the categories

            :return: A dictionary of the category\'s properties
        '''
        user_id = get_jwt_identity()

        # get BaseQuery object to allow for pagination
        the_categories = Category.query.filter_by(
            created_by=user_id).order_by("category_id desc")
        args = Q_PARSER.parse_args(request)
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
                (Category.created_by == user_id),
                (func.lower(Category.category_name).ilike("%" + q + "%")))
            # print("qqqqqqqqqqqqqqqqqqqq", the_categories.all())
            if the_categories.all():
                categorieschema = CategorySchema(many=True)
                the_categories = categorieschema.dump(the_categories)
                # print("<<<<<<<<<<<<<<<<>>>>>>>>>>>>>",
                #       the_categories.data)

                response = {"categories": the_categories.data,
                            "message": "These are the category search results"
                            }
                return response
        pag_categories = the_categories.paginate(
            page, per_page, error_out=False)

        pages = pag_categories.pages
        page = pag_categories.page

        if not pag_categories.items:
            return {'message': f'There are no categories on page {page}'}
        paginated = []
        for a_category in pag_categories.items:
            paginated.append(a_category)
        categoriesschema = CategorySchema(many=True)
        all_categories = categoriesschema.dump(paginated)
        # print("<><><><><><><><><><><><><><><>", all_categories.data)
        response = {"categories": all_categories.data,
                    "message": "These are your categories",
                    "categoryPages": pages,
                    "categoryPage": page
                    }
        return response

    @api.expect(CATEGORY)
    @api.response(201, 'Category created successfully')
    @jwt_required
    def post(self):
        ''' This method adds a new category to the DB

        :return: A dictionary with a message and status code
        '''
        user_id = get_jwt_identity()

        args = PARSER.parse_args()
        category_name = args.category_name
        description = args.description
        created_by = user_id

        validated_name = name_validator(category_name)
        if validated_name:
            category_name = category_name
            description = description

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
                'message': f'{category_name} category was created',
                'category_id': a_category.category_id
            }
            return the_response, 201
        return {'message': f'{category_name} is not a valid name. Category '
                'names can only comprise of alphabetical characters & can be '
                'more than one word'}, 400


@api.route('/<int:category_id>/')
class Categoryy(Resource):
    ''' This class handles a single category GET, PUT AND DELETE functionality
    '''

    @api.response(200, 'Category found successfully')
    @jwt_required
    def get(self, category_id):
        ''' This method returns a category '''
        user_id = get_jwt_identity()
        the_category = Category.query.filter_by(created_by=user_id,
                                                category_id=category_id).first()

        if the_category is None:
            return {'message': f'You don\'t have a category with id {category_id}'}, 404
        categoryschema = CategorySchema()
        get_response = categoryschema.dump(the_category)
        return jsonify(get_response.data)

    @api.expect(EDIT_PARSER)
    @api.response(204, 'Successfully edited')
    @jwt_required
    def put(self, category_id):
        ''' This method edits a category.

        :param str name: The new category name
        :param str description: The new category description
        :return: A dictionary with a message
        '''
        user_id = get_jwt_identity()
        args = EDIT_PARSER.parse_args()
        category_name = args.category_name
        description = args.description

        the_category = Category.query.filter_by(created_by=user_id,
                                                category_id=category_id).first()

        if not category_name:
            category_name = the_category.category_name

        if not description:
            description = the_category.description

        category_name = category_name.lower()
        description = description.lower()

        if the_category is None:
            return {'message': f'Category with id {category_id} doesn\'t exist'}

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
        return {'message': f'{category_name} is not a valid name. Category '
                'names can only comprise of alphabetical characters & can be '
                'more than one word'}

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
        return {'message': f'Category with id {category_id} does not exist'}
