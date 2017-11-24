# /instance/config.py
''' This script holds all the environment configurations  '''

import os


class Config(object):
    """ The configurations all the environments should have."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = "x7êr(9rty%$$#NV^h_=+4"
    # path to production database
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/recipe_db'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    # path to test database
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True
    SQLALCHEMY_ECHO = True  # allow SQLAlchemy to log error
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
