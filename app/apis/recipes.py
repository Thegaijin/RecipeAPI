# app/auth/recipes.py
''' This script holds the resource functionality for recipe CRUD '''

# Local imports
from app import db
from app.models.category import Category
from app.models.recipe import Recipe
from app.models.user import User
import traceback
# Third party imports
from flask import request
from flask_restplus import fields, Namespace, Resource, reqparse


api = Namespace(
    'recipes', description='Creating, viewing, editing and deleting recipes and\
    recipe categories')

category = api.model('Category', {
    'name': fields.String(required=True, description='category name'),
    'description': fields.String(required=True,
                                 description='category description'),
})

recipe = api.model('Recipe', {
    'name': fields.String(required=True, description='Recipe name'),
    'description': fields.String(required=True,
                                 description='Recipe description'),
})

# validate input
parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
parser.add_argument('name', required=True, help='Try again: {error_msg}')
parser.add_argument('description', required=True)


@api.route('/categories/')
@api.route('/categories/<id>/')
class Categories(Resource):
    ''' The class handles the Category CRUD functionality '''

    # specifies the expected input fields
    @api.expect(parser)
    def post(self):
        ''' This method adds a new category to the DB

        :param name:A string: The category name
        :param description: string: The category description
        :return: A dictionary with a message
        '''
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        return auth_header
        # get token from header (Bearer <token>)
        ''' access_token = auth_header.split(" ")[1]

        if access_token:
            # Get user id from token
            user_id = User.decode_token(access_token)

        args = parser.parse_args()
        name = args.name
        description = args.description
        created_by = user_id

        try:
            # check if the category exists
            if User.query.filter_by(name=name).first() is not None:
                category = Category(name, description, created_by)
                db.session.add(category)
                db.session.commit()
                the_response = {
                    'status': 'Successfully creation',
                    'message': 'Category was successfully created'
                }
            taceback.print_exc()
            return {'message': 'Category already exists'}
        except:
            pass
 '''
