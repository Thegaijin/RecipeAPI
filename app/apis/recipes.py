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
    'recipe_name': fields.String(required=True, description='Recipe name'),
    'description': fields.String(required=True,
                                 description='Recipe description'),
})

# validate input
parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
parser.add_argument('name', required=True, help='Try again: {error_msg}')
parser.add_argument('description', required=True)

# validate input
recipe_parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
recipe_parser.add_argument(
    'recipe_name', required=True, help='Try again: {error_msg}')
recipe_parser.add_argument('description', required=True)


@api.route('/categories')
@api.route('/categories/<name>/')
class Categories(Resource):
    ''' The class handles the Category CRUD functionality '''

    @api.response(200, 'Category found successfully')
    @jwt_required
    def get(self, name=None):
        ''' This method returns a category. The method is passed the category
            name in the url and it returns the details of that category

            :param str name: The name of the category you want to view.
            :return: A dictionary of the category\'s properties
        '''

        try:
            if name is not None:
                the_category = Category.query.filter_by(
                    name=name).one()
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
        username = get_jwt_identity()

        args = parser.parse_args()
        name = args.name
        description = args.description
        created_by = username

        try:
            # check if the category exists
            if Category.query.filter_by(name=name).first() is None:
                category = Category(name, description, created_by)
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
        ''' This method edits a category. 

        :param str name: The new category name
        :param str description: The new category description
        :return: A dictionary with a message
        '''
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

                else:
                    return {'message': 'No changes to be made'}
                return {'message': 'The category does not exist'}
        except Exception as e:

            edit_response = {
                'message': str(e)
            }
            traceback.print_exc()
            return edit_response

    @api.response(204, 'The category was successfully deleted')
    @jwt_required
    def delete(self, name):
        ''' This method deletes a Category. The method is passed the category
            name in the url and it deletes the category that matches that name.

            :param str name: The name of the category you want to delete.
            :return: A dictionary with a message confirming deletion.
        '''
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


@api.route('/recipe/<name>/')
@api.route('/recipe/<name>/<recipe_name>/')
class Recipes(Resource):
    ''' The class handles the Recipes CRUD functionality '''

    @api.response(200, 'Success')
    @jwt_required
    def get(self, name, recipe_name):
        ''' This method returns a category '''
        try:
            the_recipe = Recipe.query.filter_by(
                recipe_name=recipe_name).first()
            if the_recipe is not None:

                get_response = {}
                get_response['id'] = the_recipe.id
                get_response['name'] = the_recipe.recipe_name
                get_response['description'] = the_recipe.ingredients
                get_response['category'] = the_recipe.category_name
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
    def post(self, name):
        ''' This method adds a new recipe to the DB

        :param str name: The recipe name
        :param str description: The recipe description
        :return: A dictionary with a message
        '''

        # get current username
        username = get_jwt_identity()

        args = recipe_parser.parse_args()
        recipe_name = args.recipe_name
        description = args.description
        category_name = name
        created_by = username

        try:
            # check if the category exists
            if Recipe.query.filter_by(recipe_name=recipe_name).first() is None:
                recipe = Recipe(recipe_name, description,
                                category_name, created_by)
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
    def put(self, name, recipe_name):
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
    def delete(self, name, recipe_name):
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
