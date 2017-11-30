# user_auth.py
''' This scripy holds the flask jwt verfication and identifying functions '''

# Third party import
from werkzeug.security import safe_str_cmp

# Local import
from app.models.user import User


def authenticate(username, password):
    ''' This function authenticates the user

    :param str username: The user\'s username
    :param str password: The user\'s password
    :return obj user: The user object
    '''
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    ''' This functions picks the user ID from the token

    :param str payload: The payload from the token
    :return obj: The object matching the ID
    '''
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()
