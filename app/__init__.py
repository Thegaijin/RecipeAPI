# app/__init__.py
''' This script initialises the app through the application factory, the new
    flask object is created, loads the configuration and connects to the DB
'''

# third party imports
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restplus import Api


# local import
# importing protected configurations from /instance
from instance.config import app_config
from .db import db
from app.models.blacklist import Blacklist

jwt = JWTManager()


def create_app(config_name):
    ''' Creates an instance of the Flask class
        Loads configuration settings and connects to the required DB
        Registers the blueprint with the namespaces
        returns the instance

        :param str config_name: The key to activate the related configuration
    '''

    # Load configurations from instance folder
    app = Flask(__name__, instance_relative_config=True)

    # Updates the values from the given object
    app.config.from_object(app_config[config_name])
    # Updates the values in the config from a Python file
    app.config.from_pyfile('config.py')
    # set to False to avoid wasting resources
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # set token blacklisting to true
    app.config['JWT_BLACKLIST_ENABLED'] = True
    # set the type of token to blacklist
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    # prep application to work with SQLAlchemy
    db.init_app(app)
    jwt.init_app(app)

    # Import blueprints
    from app.apis import apiv1_blueprint as api_v1
    from app.apis import apiv2_blueprint as api_v2

    # Register blueprints
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    app.register_blueprint(api_v2, url_prefix='/api/v2')

    return app


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """ Call back function that checks if a the token is valid on all the
        endpoints that require a token

        :Decorators:
            jwt
        :param decrypted_token: -- [description]
        :Return: Boolean
    """
    jti = decrypted_token['jti']

    if Blacklist.query.filter_by(token=jti).first() is None:
        return False
    return True


@jwt.revoked_token_loader
def my_revoked_token_callback():
    return jsonify({'message': 'You must be logged in to access this page'})
