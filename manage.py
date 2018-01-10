# manage.py

import os
from unittest import TestLoader, TextTestRunner
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.db import db


app = create_app(config_name=os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
