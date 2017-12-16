# app/appis/__init__.py
''' This script aggregates the namespaces '''

# Third party import
from flask import Blueprint
from flask_restplus import Api

# Local imports
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
            description='An API ...')

# namespace for user registration and login
api.add_namespace(ns_auth)

# namespace for the categories CRUD
api.add_namespace(ns_categories)

# namespace for the recipes CRUD
api.add_namespace(ns_recipes)


# Version 2 namespaces
api_2.add_namespace(ns_hello)
