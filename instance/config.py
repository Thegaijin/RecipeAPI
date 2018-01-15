''' This script has the configuration settings for the different states '''


class Config(object):
    """ The configurations all the environments should have."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = "x7êr(9rty%$$#NV^h_=+4"
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/recipe_db'
    # RESTPLUS_VALIDATE = True


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    RESTPLUS_VALIDATE = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True
    SQLALCHEMY_ECHO = False
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
