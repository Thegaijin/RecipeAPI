# app/models/user.py
''' This scripts holds the DB table models '''

# Third party import
from flask_bcrypt import Bcrypt

# Local import
from app import db
from app.models.crudmixin import CRUDMixin


class User(db.Model, CRUDMixin):
    ''' Class representing the Users table '''

    __tablename__ = 'users'  # should always be plural

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    categories = db.relationship(
        'Category', order_by='category.id', cascade='all, delete-orphan',
        backref='users', lazy='dynamic')

    def __init__(self, username):
        ''' Initialise the user with a username '''
        self.username = username

    def password_hasher(self, password):
        ''' hashes the password '''
        self.password_hash = Bcrypt().generate_password_hash(password)

    def password_authenticator(self, password):
        ''' Compare password value against the stored hashed password '''
        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)
