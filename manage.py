''' This script manages migrations and starts the app '''

import os
from unittest import TestLoader, TextTestRunner
from flask import redirect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.db import db


# FLASK_CONFIG = development
app = create_app(config_name=os.getenv('FLASK_CONFIG'))
# print("This is the app", app)
# print("This is the app type", type(app))
# print("This is the app config", app.config)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


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


@app.route('/')
def main():
    ''' Load the documentation on heroku '''
    return redirect('/api/v1/')


if __name__ == '__main__':
    manager.run()
