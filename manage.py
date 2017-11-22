# manage.py
''' This script handles updating the DB with changes made to the models '''

# Third party imports
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# Local imports
from app import db, create_app
from app.models.user import User
from app.models.category import Category
from app.models.recipe import Recipe


app = create_app(config_name=os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)
# Tracks commands and handles how they are called from the command line
manager = Manager(app)

# adds the migration commands and enforces that they start with db
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
