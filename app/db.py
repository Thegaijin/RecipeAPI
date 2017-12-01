# db.py
''' This script initialise the sqlAlchemy instance '''

# Third party import
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT

db = SQLAlchemy()
jwt = JWT()
