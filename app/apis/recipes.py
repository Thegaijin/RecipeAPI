# app/auth/categories.py
''' This script holds the resource functionality for recipe CRUD '''

# Local imports
from app import db
# from app.models.category import Category
from app.models.recipe import Recipe
# from app.models.user import User
import traceback
# Third party imports
from flask import request
from flask_restplus import fields, Namespace, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace(
    'recipes', description='Creating, viewing, editing and deleting recipes and\
    recipe categories')

recipe = api.model('Recipe', {
    'recipe_name': fields.String(required=True, description='Recipe name'),
    'description': fields.String(required=True,
                                 description='Recipe description'),
})

# validate input
recipe_parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
recipe_parser.add_argument(
    'recipe_name', required=True, help='Try again: {error_msg}')
recipe_parser.add_argument('description', required=True)

q_parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
q_parser.add_argument('q', help='search')
q_parser.add_argument('page', type=int, help='Try again: {error_msg}')
q_parser.add_argument('per_page', type=int, help='Try again: {error_msg}')


@api.route('/<int:category_id>/')
@api.route('/<int:category_id>/<recipe_name>/')
class Recipes(Resource):
    ''' The class handles the Recipes CRUD functionality '''

    @api.response(200, 'Success')
    @jwt_required
    def get(self, category_id, recipe_name):
        ''' This method returns a recipe '''
        try:
            the_recipe = Recipe.query.filter_by(
                recipe_name=recipe_name).first()
            if the_recipe is not None:

                get_response = {}
                get_response['recipe_id'] = the_recipe.recipe_id
                get_response['recipe_name'] = the_recipe.recipe_name
                get_response['description'] = the_recipe.ingredients
                get_response['category_name'] = the_recipe.category_name
                get_response['created by'] = the_recipe.created_by
                return get_response, 200

        except Exception as e:
            get_response = {
                'message': str(e)
            }

            return get_response, 404

    # specifies the expected input fields
    @api.expect(recipe_parser)
    @api.response(201, 'Success')
    @jwt_required
    def post(self, category_id):
        ''' This method adds a new recipe to the DB

        :param str name: The recipe name
        :param str description: The recipe description
        :return: A dictionary with a message
        '''

        # get current username
        user_id = get_jwt_identity()

        args = recipe_parser.parse_args()
        recipe_name = args.recipe_name
        print('recipe name: {}'.format(recipe_name))
        description = args.description
        print('description: {}'.format(description))
        category_id = category_id
        created_by = user_id

        try:
            # check if the category exists
            if Recipe.query.filter_by(created_by=created_by,
                                      category_id=category_id,
                                      recipe_name=recipe_name).first() is None:
                recipe = Recipe(recipe_name, description,
                                category_id, created_by)
                print(recipe)
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

    @api.expect(recipe_parser)
    @api.response(204, 'Success')
    @jwt_required
    def put(self, category_id, recipe_name):
        ''' This method edits a recipe

        :param str recipe_name: The new recipe name
        :param str description: The new recipe description
        :return: A dictionary with a message
        '''
        try:
            the_recipe = Recipe.query.filter_by(
                recipe_name=recipe_name).first()
            if the_recipe is not None:
                args = recipe_parser.parse_args()
                recipe_name = args.recipe_name
                description = args.description

                if recipe_name is not None and description is not None:
                    the_recipe.recipe_name = recipe_name
                    the_recipe.ingredients = description
                    db.session.add(the_recipe)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Recipe details successfully edited'
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
    def delete(self, category_id, recipe_name):
        ''' This method deletes a Recipe '''
        try:
            the_recipe = Recipe.query.filter_by(
                recipe_name=recipe_name).first()
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
