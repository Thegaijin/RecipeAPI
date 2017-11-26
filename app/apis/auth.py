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
    ''' This class registers a new user. '''

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class UserLogin(Resource):
    ''' This class logs in an existing user. '''

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


''' class UserAPI(Resource):
    

    # POST methods map to this function
    def post(self):
        Responds to POST requests at the / auth / register view
        # check if a username already exists
        #user = User.query.filter_by(username=request.data['username']).first()
        pass
 '''
