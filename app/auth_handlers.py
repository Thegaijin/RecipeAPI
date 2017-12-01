# user_auth.py
''' This scripy holds the flask jwt verfication and identifying functions '''

# Third party import
from flask_bcrypt import Bcrypt
# from werkzeug.security import safe_str_cmp

# Local import
from app.models.user import User
from .db import jwt


@jwt.authentication_handler
def authenticate(username, password):
    ''' This function authenticates the user

    :param str username: The user\'s username
    :param str password: The user\'s password
    :return obj user: The user object
    '''

    user = User.query.filter_by(username=username).first()
    print(user)
    if Bcrypt().check_password_hash(user.password, password):
        return user


@jwt.identity_handler
def identify(payload):
    return User.query.filter_by(id=payload['identity']).scalar()
