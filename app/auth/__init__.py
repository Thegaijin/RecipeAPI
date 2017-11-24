# app/auth/__init__.py
''' This script creates the Blueprint object and initializes it with a name '''

from flask import Blueprint
# instance of Blueprint representing authentication blueprint
auth = Blueprint('auth', __name__)

# imported at the bottom to deal with circular imports issue
from . import views
