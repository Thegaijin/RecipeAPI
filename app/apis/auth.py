# app/auth/user.py
''' This script holds the resource functionality for user creation and login '''

# Local imports
from app import db
from app.models.user import User


# Third party imports
from flask import jsonify, make_response, request
from flask_restplus import fields, Namespace, Resource, reqparse


api = Namespace(
    'auth', description='Creating and authenticating user credentials')

user = api.model('User', {
    'username': fields.String(required=True, description='user\'s name'),
    'password': fields.String(required=True, description='user\'s  password'),
})


@api.route('/auth/register')
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
