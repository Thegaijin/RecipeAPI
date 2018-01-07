# app/auth/categories.py
''' This script holds the resource functionality for recipe CRUD '''


# Third party imports
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import fields, Namespace, Resource, reqparse

# Local imports
from app import db
from app.models.recipe import Recipe
from ..validation_helper import name_validator
from ..get_helper import (per_page_max, per_page_min,
                          manage_get_recipes, manage_get_recipe)


api = Namespace(
    'recipes', description='Creating, viewing, editing and deleting recipes')

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
recipe_parser.add_argument('description', required=True, default='')

q_parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
q_parser.add_argument('q', help='search', location='args')
q_parser.add_argument(
    'page', type=int, help='Try again: {error_msg}', location='args')
q_parser.add_argument('per_page', type=int,
                      help='Try again: {error_msg}', location='args')


@api.route('')
class Recipess(Resource):
    ''' The class handles the view functionality for all recipes '''

    @api.response(200, 'Success')
    @api.expect(q_parser)
    @jwt_required
    def get(self):
        ''' A method to get all the recipes
            Returns all the recipes created by a user or a recipe that matches
            a search keyword

            :return: A recipe that matches the search or a list of recipe\'s
        '''
        try:
            user_id = get_jwt_identity()
            the_recipes = Recipe.query.filter_by(created_by=user_id)
            args = q_parser.parse_args(request)
            return manage_get_recipes(the_recipes, args)
        except Exception as e:
            get_response = {
                'View recipes exception': str(e)
            }
            return get_response


@api.route('/<int:category_id>/')
class Recipes(Resource):
    ''' The class handles the Recipes CRUD functionality '''

    @api.response(200, 'Success')
    @api.expect(q_parser)
    @jwt_required
    def get(self, category_id):
        ''' A method to get recipes in a category.
            Checks if a category ID exists and returns all the recipes in the
            category or one with a recipe_name that matches a search keyword

            :param int category_id: The category id to which the recipe belongs
            :return: A recipe that matches the search keyword or all the
            recipes in a category
        '''
        try:
            user_id = get_jwt_identity()
            the_recipes = Recipe.query.filter_by(
                created_by=user_id, category_id=category_id)
            args = q_parser.parse_args(request)
            return manage_get_recipes(the_recipes, args)
        except Exception as e:
            get_response = {
                'View recipes in category exception': str(e)
            }
            return get_response, 404

    # specifies the expected input fields
    @api.expect(recipe)
    @api.response(201, 'Success')
    @jwt_required
    def post(self, category_id):
        ''' A method to create a recipe.
            Checks if a recipe name exists in the given category, if it
            doesn\'t it creates the new recipe,if it does,it returns a message

            :param int category_id: The category id to which the recipe belongs
            :return: A dictionary with a message and status code
        '''

        # get current username
        user_id = get_jwt_identity()
        args = recipe_parser.parse_args()
        recipe_name = args.recipe_name
        description = args.description
        category_id = category_id
        created_by = user_id

        validated_name = name_validator(recipe_name)
        if len(validated_name) is len(recipe_name):
            try:
                # change values to lowercase
                recipe_name = recipe_name.lower()
                description = description.lower()

                # check if the category exists
                if Recipe.query.filter_by(created_by=created_by,
                                          category_id=category_id,
                                          recipe_name=recipe_name).first() is None:
                    a_recipe = Recipe(recipe_name, description,
                                      category_id, created_by)
                    db.session.add(a_recipe)
                    db.session.commit()
                    the_response = {
                        'status': 'Success',
                        'message': 'Recipe has been created',
                        'recipe_name': a_recipe.recipe_name
                    }
                    return the_response, 201
                return {'message': 'Recipe already exists'}
            except Exception as e:
                post_response = {
                    'Add recipe exception': str(e)
                }
                return post_response
        else:
            return {'Input validation Error': 'The recipe name should '
                    'comprise of alphabetical characters and can be more than '
                    'one word'}


@api.route('/<int:category_id>/<recipe_name>/')
class Recipee(Resource):
    """This class handles a single recipe GET, PUT AND DELETE functionality
    """

    @api.response(200, 'Category found successfully')
    @jwt_required
    def get(self, category_id, recipe_name):
        ''' A method to get a recipe in a category by name.
            Checks if the given recipe name exists in the given category and
            returns the recipe details.

            :param int category_id: The category id to which the recipe belongs
            :param str recipe_name: The name of the recipe to search for
            :return: The details of the recipe
        '''
        try:
            the_recipe = Recipe.query.filter_by(
                category_id=category_id, recipe_name=recipe_name).first()
            if the_recipe is not None:
                return manage_get_recipe(the_recipe)
            return {'message': 'The recipe does not exist'}
        except Exception as e:
            get_response = {
                'View recipe by name exception': str(e)
            }
            return get_response, 404

    @api.expect(recipe_parser)
    @api.response(204, 'Success')
    @jwt_required
    def put(self, category_id, recipe_name):
        ''' A method for editing a recipe.
            Checks if the given recipe name exists in the given category and
            edits it with the new details.

            :param str recipe_name: The new recipe name
            :param str description: The new recipe description
            :return: A dictionary with a message
        '''
        try:
            the_recipe = Recipe.query.filter_by(category_id=category_id,
                                                recipe_name=recipe_name).first()
            # check of recipe to be edited exists
            if the_recipe is not None:
                args = recipe_parser.parse_args()
                recipe_name = args.recipe_name
                description = args.description

                # change the values to lowercase
                recipe_name = recipe_name.lower()
                description = description.lower()

                # check if there's a new value is added otherwise keep previous
                if not recipe_name:
                    recipe_name = the_recipe.recipe_name
                if not description:
                    description = the_recipe.ingredients

                validated_name = name_validator(recipe_name)
                if len(validated_name) is len(recipe_name):
                    the_recipe.recipe_name = recipe_name
                    the_recipe.ingredients = description
                    db.session.add(the_recipe)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Recipe details successfully edited'
                    }
                    return edit_response, 200
                else:
                    return {'Input validation Error': 'The recipe name should '
                            'comprise of alphabetical characters and can be '
                            'more than one word'}
            return {'message': 'The recipe does not exist'}
        except Exception as e:
            edit_response = {
                'Edit recipe exception': str(e)
            }
            return edit_response

    @api.response(204, 'Success')
    @jwt_required
    def delete(self, category_id, recipe_name):
        ''' A method to delete a recipe
            Checks if the given recipe name exists in the given category and
            deletes it.

            :param str recipe_name: The new recipe name
            :param str description: The new recipe description
            :return: A dictionary with a message
        '''
        try:
            the_recipe = Recipe.query.filter_by(category_id=category_id,
                                                recipe_name=recipe_name).first()
            if the_recipe is not None:
                db.session.delete(the_recipe)
                db.session.commit()
                return {'message': 'Recipe was deleted'}
            return {'message': 'The recipe does not exist'}
        except Exception as e:
            delete_response = {
                'Delete recipe exception': str(e)
            }
            return delete_response
