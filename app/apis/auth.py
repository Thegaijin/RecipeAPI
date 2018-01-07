# app/auth/user.py
''' This script holds resource functionality for user creation and login '''

# Third party imports
from datetime import timedelta
import re
from flask import request, jsonify
from flask_jwt_extended import (
    get_jwt_identity, create_access_token, jwt_required, get_raw_jwt)
from flask_restplus import fields, Namespace, Resource, reqparse


# Local imports
from app.models.user import User
from app.models.blacklist import Blacklist
from ..db import db
from ..validation_helper import username_validator, password_validator


api = Namespace(
    'auth', description='Creating and authenticating user credentials')

user = api.model('User', {
    'username': fields.String(required=True,
                              description='user\'s name'),
    'password': fields.String(required=True, description='user\'s password'),
})

# validate input
parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
parser.add_argument('username',
                    required=True, help='Try again: {error_msg}')
parser.add_argument('password', required=True)


@api.route('/register/')
class UserRegistration(Resource):
    ''' This class registers a new user. '''

    # specifies the expected input fields
    @api.expect(user)  # , validate=True
    @api.response(201, 'Account was successfully created')
    def post(self):
        ''' This method adds a new user.
            Takes the user credentials added, hashes the password and saves
            them to the DB

            :return: A dictionary with a message
        '''

        args = parser.parse_args()
        username = args.username
        password = args.password

        validated_username = username_validator(username)
        validated_password = password_validator(password)
        if validated_username and validated_password:
            try:
                username = username.lower()
                # check if the already username exists in the db
                if User.query.filter_by(username=username).first() is None:
                    new_user = User(username)
                    # hash the password
                    new_user.password_hasher(password)
                    # add to the db
                    db.session.add(new_user)
                    db.session.commit()

                    return {'message': 'Account was successfully created'}, 201
                return {'message': 'The username already exists'}, 202
            except:
                return {'message': 'Error occured during user registration'}, 400
        else:
            return {'Input validation error': 'username can only comprise '
                    'of alphanumeric values & an underscore. '
                    'Password can only comprise of alphanumeric values '
                    '& an underscore and between 6 to 25 characters long'}


@api.route('/login/')
class UserLogin(Resource):
    ''' This class logs in an existing user. '''

    @api.expect(user)
    @api.response(201, 'You have been signed in')
    def post(self):
        ''' This method signs in an existing user
            Checks if the entered credentials match the existing ones in the DB
            and if they do, gives the user access.

            :return: A dictionary with a message
        '''
        args = parser.parse_args()
        username = args.username
        password = args.password

        try:
            # check if the user exists
            if User.query.filter_by(username=username).first() is not None:
                # save user object
                the_user = User.query.filter_by(username=username).first()
                # check if the password matches, returns True if they match
                a_user = the_user.password_checker(password)

                if a_user:
                    expires = timedelta(days=365)
                    access_token = create_access_token(
                        identity=the_user.user_id, expires_delta=expires)

                    the_response = {
                        'status': 'successful Login',
                        'message': 'You have been signed in',
                        'access_token': access_token
                    }
                    return the_response, 200
                return {'Login error': 'Credentials do not match, try again'}, 401
            return {'Login error': 'Username does not exist, signup'}, 401
        except:
            return {'Login exception': 'An error occured while attempting'
                    'to login'}


@api.route('/logout/')
class UserLogout(Resource):
    ''' This class logs out a currently logged in user. '''

    @api.response(200, 'You have been logged out')
    @jwt_required
    def delete(self):
        ''' This method logs out a logged in user
            Checks if the logged users token is valid.

            :return: A dictionary with a message
        '''
        try:
            jti = get_raw_jwt()['jti']
            blacklisted = Blacklist(jti)
            db.session.add(blacklisted)
            db.session.commit()
            the_response = {"message": "Successfully logged out"}
            return the_response, 200
        except Exception as e:
            blacklist_response = {
                'Logout Error': str(e)
            }
            return blacklist_response
