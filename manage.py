# manage.py
''' This script handles updating the DB with changes made to the models '''

# Third party imports
import os
from unittest import TestLoader, TextTestRunner
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# Local imports
from app import create_app
from app.models.user import User
from app.models.category import Category
from app.models.recipe import Recipe
from app.db import db


app = create_app(config_name=os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)

# Tracks commands and handles how they are called from the command line
manager = Manager(app)

# adds the migration commands and enforces that they start with db
manager.add_command('db', MigrateCommand)

# The decorator allows us to define a command called "test"
# Usage: python manage.py test


@manager.command
def test():
    """Runs the unit tests without test coverage."""

    # load the tests from the tests folder
    tests = TestLoader().discover('./tests', pattern='test*.py')
    # run the tests
    result = TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
