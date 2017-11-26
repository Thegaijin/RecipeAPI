# app/auth/recipes.py
''' This script holds the resource functionality for recipe CRUD '''

# Local imports
from app.models.category import Category
from app.models.recipe import Recipe

# Third party imports
from flask import jsonify, make_response, request
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
