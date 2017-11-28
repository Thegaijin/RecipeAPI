# app/auth/user.py
''' This script holds the resource functionality for user creation and login '''

# Local imports
from app import db
from app.models.user import User


# Third party imports
from flask import jsonify, make_response, request
from flask_restplus import fields, Namespace, Resource, reqparse
import traceback


api = Namespace(
    'auth', description='Creating and authenticating user credentials')

user = api.model('User', {
    'username': fields.String(required=True,
                              pattern="[^a-zA-Z0-9]",
                              description='user\'s name'),
    'password': fields.String(required=True, description='user\'s password'),
})

# validate input
parser = reqparse.RequestParser(bundle_errors=True)
# specify parameter names and accepted values
parser.add_argument('username', required=True, help='Try again: {error_msg}')
parser.add_argument('password', required=True)


@api.route('/register/')
class UserRegistration(Resource):
    ''' This class registers a new user. '''

    # specifies the expected input fields
    @api.expect(parser)
    def post(self):
        ''' This method adds a new user to the DB

        :param username:A string: The user\'s chosen name
        :param password: string: The user\'s password
        '''

        args = parser.parse_args()
        username = args.username
        password = args.password

        try:
            # check if the already username exists in the db
            if User.query.filter_by(username=username).first() is None:
                new_user = User(username)
                # hash the password
                new_user.password_hasher(password)
                # add to the db
                db.session.add(new_user)
                db.session.commit()

                return {'message': '{}, Your account was successfully created\
                        '.format(new_user.username)}, 201
                # the_response = {'message': '{}, Your account was successfully\
                #        created'.format(new_user.username)}
                # return make_response(jsonify(the_response)), 201
            return {'message': 'The username already exists'}, 400
        except:

            return {'message': 'An error occured during the user registration'}


@api.route('/login/')
class UserLogin(Resource):
    ''' This class logs in an existing user. '''

    @api.expect(parser)
    def post(self):
        ''' This method signs in an existing user

        :param username: A string: The user\'s chosen name
        :param password: A string: The user\'s password
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
                password_match = the_user.password_checker(password)
                if password_match:
                    user_token = the_user.generate_token(the_user.id)
                    the_response = {
                        'status': 'successful Login',
                        'message': 'Welcome, {}'.format(the_user.username),
                        'token': user_token
                    }
                    return the_response, 200
                return {'message': 'Credentials do not match, please try again'}
            return {'message': 'Username does not exist, please signup'}
        except:
            traceback.print_exc()
            return {'message': 'An error occured while attempting to login'}
