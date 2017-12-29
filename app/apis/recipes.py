# app/auth/categories.py
''' This script holds the resource functionality for recipe CRUD '''


# Third party imports
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import fields, Namespace, Resource, reqparse

# Local imports
from app import db
from app.models.recipe import Recipe
from ..serializers import RecipeSchema
from .categories import per_page_max, per_page_min


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
q_parser.add_argument('q', help='search', location='args')
q_parser.add_argument(
    'page', type=int, help='Try again: {error_msg}', location='args')
q_parser.add_argument('per_page', type=int,
                      help='Try again: {error_msg}', location='args')


@api.route('/<int:category_id>/')
class Recipes(Resource):
    ''' The class handles the Recipes CRUD functionality '''

    @api.response(200, 'Success')
    @api.expect(q_parser)
    @jwt_required
    def get(self, category_id=None):
        ''' This method returns all the recipes created by a user or a
            category that mateches a search keyword

            :return: A recipe that matches the search or a list of recipe\'s
        '''
        try:
            user_id = get_jwt_identity()

            print('user id', user_id)
            if category_id is None:
                the_recipes = Recipe.query.filter_by(
                    created_by=user_id)
                print('if none', the_recipes)
            the_recipes = Recipe.query.filter_by(
                created_by=user_id, category_id=category_id)
            print('if not none', the_recipes)

            args = q_parser.parse_args(request)
            q = args.get('q', '')
            page = args.get('page', 5)
            per_page = args.get('per_page', 10)
            if per_page < per_page_min:
                per_page = per_page_min

            if per_page > per_page_max:
                per_page = per_page_max

            if q:
                q = q.lower()
                for a_recipe in the_recipes.all():
                    if q in a_recipe.recipe_name.lower():

                        recipeschema = RecipeSchema()
                        the_recipe = recipeschema.dump(a_recipe)

                        return jsonify(the_recipe.data)

            pag_recipes = the_recipes.paginate(
                page, per_page, error_out=False)

            paginated = []
            for a_recipe in pag_recipes.items:
                paginated.append(a_recipe)
            recipesschema = RecipeSchema(many=True)

            all_recipes = recipesschema.dump(paginated)
            print('all recipes', all_recipes)

            return jsonify(all_recipes)

        except Exception as e:
            get_response = {
                'message': str(e)
            }

            return get_response, 404

    # specifies the expected input fields
    @api.expect(recipe)
    @api.response(201, 'Success')
    @jwt_required
    def post(self, category_id):
        ''' This method adds a new recipe to the DB

        :param str category_id: The category name to which the recipe belongs
        :return: A dictionary with a message and status code
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
                a_recipe = Recipe(recipe_name.lower(), description.lower(),
                                  category_id, created_by)
                print(recipe)
                db.session.add(a_recipe)
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

            return post_response


@api.route('/<int:category_id>/<recipe_name>/')
class Recipee(Resource):
    """This class handles a single recipe GET, PUT AND DELETE functionality
    """

    @api.response(200, 'Category found successfully')
    @jwt_required
    def get(self, category_id, recipe_name):
        ''' This method returns a recipe in a paerticular category
        '''
        try:
            the_recipe = Recipe.query.filter_by(
                category_id=category_id, recipe_name=recipe_name).first()

            if the_recipe is not None:

                recipeschema = RecipeSchema()
                get_response = recipeschema.dump(the_recipe)
                return jsonify(get_response.data)
        except Exception as e:
            get_response = {
                'message': str(e)
            }

            return get_response, 404

    @api.expect(recipe)
    @api.response(204, 'Success')
    @jwt_required
    def put(self, category_id, recipe_name):
        ''' This method edits a recipe

        :param str recipe_name: The new recipe name
        :param str description: The new recipe description
        :return: A dictionary with a message
        '''
        try:
            the_recipe = Recipe.query.filter_by(category_id=category_id,
                                                recipe_name=recipe_name).first()
            if the_recipe is not None:
                args = recipe_parser.parse_args()
                recipe_name = args.recipe_name
                description = args.description

                if recipe_name is not None and description is not None:
                    the_recipe.recipe_name = recipe_name.lower()
                    the_recipe.ingredients = description.lower()
                    db.session.add(the_recipe)
                    db.session.commit()
                    edit_response = {
                        'status': 'Success',
                        'message': 'Recipe details successfully edited'
                    }

                    return edit_response, 204
                return {'message': 'No changes to be made'}
            return {'message': 'The recipe does not exist'}
        except Exception as e:

            edit_response = {
                'message': str(e)
            }

            return edit_response

    @api.response(204, 'Success')
    @jwt_required
    def delete(self, category_id, recipe_name):
        ''' This method deletes a Recipe '''
        try:
            the_recipe = Recipe.query.filter_by(category_id=category_id,
                                                recipe_name=recipe_name).first()
            if the_recipe is not None:
                db.session.delete(the_recipe)
                db.session.commit()
                return {'message': 'The recipe was successfully deleted'}
            return {'message': 'The recipe does not exist'}
        except Exception as e:

            delete_response = {
                'message': str(e)
            }

            return delete_response
