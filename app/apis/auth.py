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

register_user = api.model('User', {
    'username': fields.String(required=True,
                              description='user\'s name'),
    'password': fields.String(required=True, description='user\'s password'),
    'email': fields.String(required=True, description='user\'s email')
})

login_user = api.model('User', {
    'username': fields.String(required=True,
                              description='user\'s name'),
    'password': fields.String(required=True, description='user\'s password')
})

parser = reqparse.RequestParser(bundle_errors=True)
<< << << < HEAD
parser.add_argument('username',
                    required=True, help='Try again: {error_msg}')
== == == =
parser.add_argument('username', required=True)
>>>>>> > validate
parser.add_argument('password', required=True)
parser.add_argument('email', required=True)

login_parser = reqparse.RequestParser(bundle_errors=True)
login_parser.add_argument('username', required=True)
login_parser.add_argument('password', required=True)

auth_parser = reqparse.RequestParser(bundle_errors=True)
auth_parser.add_argument('old_password', required=True)
auth_parser.add_argument('new_password', required=True)

auth_parser = reqparse.RequestParser(bundle_errors=True)
auth_parser.add_argument('old_password', required=True)
auth_parser.add_argument('new_password', required=True)


@api.route('/register/')
class UserRegistration(Resource):
    ''' This class registers a new user. '''

    @api.expect(register_user)
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
        email = args.email

        validated_username = username_validator(username)
        validated_password = password_validator(password)
        validated_email = email_validator(email)
        if validated_username is False:
            return {"message": "username should comprise of alphanumeric "
                    "values & an underscore."}

        if validated_password is False:
            return {"message": "Password can only comprise of alphanumeric "
                    "values & an underscore and not more than 25 characters"}

        if validated_email is False:
            return {"message": "email can only comprise of alphanumeric "
                    "values & a dot as well other standard email conventions"}


<< << << < HEAD
                return {"message": "Account was successfully created"}, 201
            return {"message": "The username already exists"}, 409
        return {"message": "username can only comprise of alphanumeric values "
                "& an underscore. Password can only comprise of alphanumeric "
                "values & an underscore and between to 25 characters long"}
=======
        username = username.lower()
        if User.query.filter_by(username=username).first() is None:
            new_user = User(username, email)
            new_user.password_hasher(password)
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Account was successfully created"}, 201
        return {"message": "The username already exists"}, 409
>>>>>>> validate


@api.route('/login/')
class UserLogin(Resource):
    ''' This class logs in an existing user. '''

    @api.expect(login_user)
    @api.response(201, 'You have been signed in')
    def post(self):
        ''' This method signs in an existing user
            Checks if the entered credentials match the existing ones in the DB
            and if they do, gives the user access.

            :return: A dictionary with a message
        '''
        print('we are in the login route')
        args = login_parser.parse_args()
        username = args.username
        password = args.password
        print('the login args', args)
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
            return {'Login error': 'Credentials do not match, try again'}, 401
        return {'Login error': 'Username does not exist, signup'}, 401


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

    @api.expect(auth_parser)
    @api.response(200, 'Password reset successfully')
    @jwt_required
    def put(self):

        user_id = get_jwt_identity()
        current_user = User.query.filter_by(user_id=user_id).first()
        args = auth_parser.parse_args()
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
