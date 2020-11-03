''' This script handles user registration, login, logout and password reset '''

from datetime import timedelta
from flask_jwt_extended import (
    get_jwt_identity, create_access_token, jwt_required, get_raw_jwt)
from flask_restplus import fields, Namespace, Resource, reqparse


from app.models.user import User
from app.models.blacklist import Blacklist
from ..db import db
from ..validation_helper import(
    username_validator, password_validator, email_validator)


api = Namespace(
    'auth', description='Creating and authenticating user credentials')

REGISTER_USER = api.model('RegisterUser', {
    'username': fields.String(required=True,
                              description='user\'s name'),
    'password': fields.String(required=True, description='user\'s password'),
    'email': fields.String(required=True, description='user\'s email')
})

LOGIN_USER = api.model('LoginUser', {
    'username': fields.String(required=True,
                              description='user\'s name'),
    'password': fields.String(required=True, description='user\'s password')
})

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('username', required=True)
PARSER.add_argument('password', required=True)
PARSER.add_argument('email', required=True)

LOGIN_PARSER = reqparse.RequestParser(bundle_errors=True)
LOGIN_PARSER.add_argument('username', required=True)
LOGIN_PARSER.add_argument('password', required=True)

AUTH_PARSER = reqparse.RequestParser(bundle_errors=True)
AUTH_PARSER.add_argument('old_password', required=True)
AUTH_PARSER.add_argument('new_password', required=True)


@api.route('/register/')
class UserRegistration(Resource):
    ''' This class registers a new user. '''

    @api.expect(REGISTER_USER)
    @api.response(201, 'Account was successfully created')
    def post(self):
        ''' This method adds a new user.
            Takes the user credentials added, hashes the password and saves
            them to the DB
            :return: A dictionary with a message
        '''

        args = PARSER.parse_args()
        username = args.username
        password = args.password
        email = args.email

        validated_username = username_validator(username)
        validated_password = password_validator(password)
        validated_email = email_validator(email)
        if validated_username is False:
            return {"message": f"{username} is not a valid username. It should "
                    "comprise of alphanumeric values & an underscore."}

        if validated_password is False:
            return {"message": "Password can only comprise of alphanumeric "
                    "values & an underscore and not more than 25 characters"}

        if validated_email is False:
            return {"message": f"{email} is not a valid email. It should "
                    "comprise of alphanumeric values & a dot as well other "
                    "standard email conventions"}

        username = username.lower()
        email = email.lower()
        if User.query.filter_by(username=username).first() is not None:
            return {"message": f"The username {username} already exists"}, 409
        if User.query.filter_by(email=email).first() is not None:
            return {"message": f"The email {email} already exists"}, 409
        new_user = User(username, email)
        new_user.password_hasher(password)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Account was successfully created"}, 201


@api.route('/login/')
class UserLogin(Resource):
    ''' This class logs in an existing user. '''

    @api.expect(LOGIN_USER)
    @api.response(201, 'You have been signed in')
    def post(self):
        ''' This method signs in an existing user
            Checks if the entered credentials match the existing ones in the DB
            and if they do, gives the user access.
            :return: A dictionary with a message
        '''
        args = LOGIN_PARSER.parse_args()
        username = args.username
        password = args.password
        username = username.lower()
        if User.query.filter_by(username=username).first() is not None:
            the_user = User.query.filter_by(username=username).first()
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
            return {'message': 'Credentials do not match, try again'}, 401
        return {'message': 'Username does not exist, signup'}, 401


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
        jti = get_raw_jwt()['jti']
        blacklisted = Blacklist(jti)
        db.session.add(blacklisted)
        db.session.commit()
        the_response = {"message": "Successfully logged out"}
        return the_response, 200


@api.route('/reset_password/')
class ResetPassword(Resource):
    ''' This class logs out a currently logged in user. '''

    @api.expect(AUTH_PARSER)
    @api.response(200, 'Password reset successfully')
    @jwt_required
    def put(self):
        ''' This method handles password reset.

            :return: A dictionary with a message
        '''
        user_id = get_jwt_identity()
        current_user = User.query.filter_by(user_id=user_id).first()
        args = AUTH_PARSER.parse_args()
        old_password = args.old_password
        new_password = args.new_password

        match = current_user.password_checker(old_password)
        if password_validator(new_password):
            if not match:
                return {'message': 'The passwords did not match'}
            current_user.password_hasher(new_password)

            db.session.add(current_user)
            db.session.commit()
            return {'message': 'Password reset successfully'}
        return {'message': 'Password can only comprise of alphanumeric values '
                '& an underscore and between 6 to 25 characters long'}
