# app/auth/user.py
''' This script holds the resource functionality for user creation and login '''

# Local imports
from . import auth
from app import db, api
from app.models.user import User
from app.models.category import Category
from app.models.recipe import Recipe


# Third party imports
from flask import make_response, request, jsonify
from flask_restplus import Resource, reqparse


class UserRegistration(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class Login(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class UserAPI(MethodView):
    ''' This class registers a new user. '''

    # POST methods map to this function
    def post(self):
        ''' Responds to POST requests at the /auth/register view '''
        # check if a username already exists
        user = User.query.filter_by(username=request.data['username']).first()
