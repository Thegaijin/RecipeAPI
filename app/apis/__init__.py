# app/appis/__init__.py
''' This script aggregates the namespaces '''

# Third party import
from flask import Blueprint
from flask_restplus import Api

# Local imports
from .auth import api as ns_auth
from .recipes import api as ns_recipes

apiv1_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api = Api(apiv1_blueprint,
          title='Recipes API',
          version='1.0',
          description='An API to create, read, update and delete recipes')

# namespace for user registration and login
api.add_namespace(ns_auth)

# namespace for the recipes CRUD
api.add_namespace(ns_recipes)
