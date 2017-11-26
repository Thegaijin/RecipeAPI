# app/appis/__init__.py
''' This script aggregates the namespaces '''

# Third party import
from flask_restplus import Api

api = Api(title='Recipes API',
          version='1.0',
          description='An API to create, read, update and delete recipes')
# namespace for user registration and login
from .auth import api as ns_auth
api.add_namespace(ns_auth)

# namespace for the recipes CRUD
from .recipes import api as ns_recipes
api.add_namespace(ns_recipes)


api.add_namespace(ns_auth)
api.add_namespace(ns_recipes)
