# app/__init__.py
''' This script initialises the app through the application factory, which
    creates the new flask object,loads the configuration and connects to the DB
'''

# third party imports
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# local import
# importing protected configurations from /instance
from instance.config import app_config

# object to interact with the Database
db = SQLAlchemy()


def create_app(config_name):
    ''' Creates an instance of the FlaskAPI class
        Loads configuration settings and connects to the required DB
        returns the instance
    '''

    # Load configurations from instance folder
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    # Updates the values from the given object
    app.config.from_object(app_config[config_name])
    # Updates the values in the config from a Python file
    app.config.from_pyfile('config.py')
    # set to False to avoid wasting resources
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # connect to the DB
    db.init_app(app)

    # the app instance used to start the app
    return app
