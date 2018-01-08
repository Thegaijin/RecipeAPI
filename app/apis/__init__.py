# app/appis/__init__.py
''' This script aggregates the namespaces '''

# Third party import
from flask import Blueprint, jsonify, make_response
from flask_restplus import Api


# Local imports
from app import jwt
from .auth import api as ns_auth
from .categories import api as ns_categories
from .recipes import api as ns_recipes
from .hello import api as ns_hello


apiv1_blueprint = Blueprint('api_v1', __name__)
apiv2_blueprint = Blueprint('api_v2', __name__)

api = Api(apiv1_blueprint,
          title='Recipes API',
          version='1.0',
          description='An API to create, read, update and delete recipes')

api_2 = Api(apiv2_blueprint,
            title='My app',
            version='2.0',
            description='Another API version')

# namespace for user registration and login
api.add_namespace(ns_auth)

# namespace for the categories CRUD
api.add_namespace(ns_categories)

# namespace for the recipes CRUD
api.add_namespace(ns_recipes)

# Version 2 namespaces
api_2.add_namespace(ns_hello)

jwt._set_error_handler_callbacks(api)


@apiv1_blueprint.app_errorhandler(404)
def handle_custom_exception(e):
    '''Return a custom message and 400 status code'''
    return make_response(jsonify({'message': 'The URL does not exist'}), 404)
