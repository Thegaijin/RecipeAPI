# app/models/__init__.py
''' This script  enables database migrations for the new model and makes it
    easier to import in user.
'''
# Local Imports

from app.models.user import User              # noqa (so linter ignores the imports)
from app.models.category import Category      # noqa
from app.models.recipe import Recipe          # noqa
from . import auth
