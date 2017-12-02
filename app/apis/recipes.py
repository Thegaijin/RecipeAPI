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
from flask_jwt_extended import jwt_required, get_jwt_identity


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
@api.route('/categories/<name>/')
class Categories(Resource):
    ''' The class handles the Category CRUD functionality '''

    @api.response(200, 'Category found successfully')
    @jwt_required
    def get(self, name):
        ''' This method returns a category '''
        try:
            the_category = Category.query.filter_by(name=name).first()
            if the_category is not None:

                ''' return jsonify(id=the_category.id,
                               name=the_category.name,
                               description=the_category.description), 200 '''
                get_response = {}
                get_response['id'] = the_category.id
                get_response['name'] = the_category.name
                get_response['description'] = the_category.description
                return get_response, 200

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

        :param name:A string: The category name
        :param description: string: The category description
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
                category = Category(name, description,
                                    created_by)  # add created_by
                db.session.add(category)
                db.session.commit()
                the_response = {
                    'status': 'Success',
                    'message': 'Category was successfully created'
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
    def put(self, name=None, description=None):
        ''' This method edits a category '''
        try:
            the_category = Category.query.filter_by(name=name).first()
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
                elif name is not None and description is None:
                    the_category.name = name
                    db.session.add(the_category)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Category name successfully edited'
                    }

                    return edit_response, 204
                elif name is None and description is not None:
                    the_category.description = description
                    db.session.add(the_category)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Category description successfully edited'
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
            return post_response

    @api.response(204, 'Success')
    @jwt_required
    def delete(self, name):
        ''' This method deletes a Category '''
        try:
            the_category = Category.query.filter_by(name=name).first()
            if the_category is not None:
                db.session.delete(the_category)
                db.session.commit()
                return {'message': 'The category was successfully deleted'}
            else:
                return {'message': 'The category does not exist'}
        except Exception as e:

            post_response = {
                'message': str(e)
            }
            traceback.print_exc()
            return post_response

########################## RECIPES ############################


@api.route('/recipes/')
@api.route('/recipes/<name>/')
class Recipes(Resource):
    ''' The class handles the Category CRUD functionality '''

    @api.response(200, 'Success')
    @jwt_required
    def get(self, name):
        ''' This method returns a category '''
        try:
            the_recipe = Recipe.query.filter_by(name=name).first()
            if the_recipe is not None:

                get_response = {}
                get_response['id'] = the_recipe.id
                get_response['name'] = the_recipe.name
                get_response['description'] = the_recipe.description
                return get_response, 200

        except Exception as e:
            get_response = {
                'message': str(e)
            }

            return get_response, 404

    # specifies the expected input fields
    @api.expect(parser)
    @api.response(201, 'Success')
    @jwt_required
    def post(self):
        ''' This method adds a new recipe to the DB

        :param name:A string: The recipe name
        :param description: string: The recipe description
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
            if Recipe.query.filter_by(name=name).first() is None:
                recipe = Recipe(name, description)  # add created_by
                db.session.add(recipe)
                db.session.commit()
                the_response = {
                    'status': 'Success',
                    'message': 'Recipe was successfully created'
                }

                return the_response, 201
            return {'message': 'Recipe already exists'}
        except Exception as e:

            post_response = {
                'message': str(e)
            }
            traceback.print_exc()
            return post_response

    @api.expect(parser)
    @api.response(204, 'Success')
    @jwt_required
    def put(self, name=None, description=None):
        ''' This method edits a recipe '''
        try:
            the_recipe = Recipe.query.filter_by(name=name).first()
            if the_recipe is not None:
                args = parser.parse_args()
                name = args.name
                description = args.description

                if name is not None and description is not None:
                    the_recipe.name = name
                    the_recipe.description = description
                    db.session.add(the_recipe)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Recipe details successfully edited'
                    }

                    return edit_response, 204
                elif name is not None and description is None:
                    the_recipe.name = name
                    db.session.add(the_recipe)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Recipe name successfully edited'
                    }

                    return edit_response, 204
                elif name is None and description is not None:
                    the_recipe.description = description
                    db.session.add(the_recipe)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Recipe description successfully edited'
                    }

                    return edit_response, 204
                else:
                    return {'message': 'No changes to be made'}
                return {'message': 'The recipe does not exist'}
        except Exception as e:

            edit_response = {
                'message': str(e)
            }
            traceback.print_exc()
            return post_response

    @api.response(204, 'Success')
    @jwt_required
    def delete(self, name):
        ''' This method deletes a Recipe '''
        try:
            the_recipe = Recipe.query.filter_by(name=name).first()
            if the_recipe is not None:
                db.session.delete(the_recipe)
                db.session.commit()
                return {'message': 'The recipe was successfully deleted'}
            else:
                return {'message': 'The recipe does not exist'}
        except Exception as e:

            post_response = {
                'message': str(e)
            }
            traceback.print_exc()
            return post_response
