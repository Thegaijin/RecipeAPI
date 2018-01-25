''' This script has the app factory of the application which loads the
    extensions and reusable packages as well as the configuration settings.
'''

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from instance.config import app_config
from app.models.blacklist import Blacklist
from .db import db
from flask_cors import CORS

cors = CORS()
jwt = JWTManager()


def create_app(config_name):
    ''' Creates an instance of the Flask class
        Loads configuration settings and connects to the required DB
        Registers the blueprint with the namespaces
        returns the instance

        :param str config_name: The key to activate the related configuration
    '''

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    from app.apis import apiv1_blueprint as api_v1
    from app.apis import apiv2_blueprint as api_v2

    app.register_blueprint(api_v1, url_prefix='/api/v1')
    app.register_blueprint(api_v2, url_prefix='/api/v2')

    return app


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """ Call back function that checks if a the token is valid on all the
        endpoints that require a token

        :param decrypted_token: -- [description]
        :Return: Boolean
    """
    jti = decrypted_token['jti']

    if Blacklist.query.filter_by(token=jti).first() is None:
        return False
    return True


@jwt.revoked_token_loader
def my_revoked_token_callback():
    ''' Checks if a user attempts to log in with revoked token '''
    return jsonify({'message': 'You must be logged in to access this page'})
