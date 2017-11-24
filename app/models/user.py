# app/models/user.py
''' This scripts holds the DB table models '''

# Third party import
from datetime import datetime, timedelta
from flask import current_app
from flask_bcrypt import Bcrypt
import jwt

# Local import
from app import db
from app.models.crudmixin import CRUDMixin


class User(db.Model, CRUDMixin):
    ''' Class representing the Users table '''

    __tablename__ = 'users'  # should always be plural

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    categories = db.relationship(
        'Category', order_by='category.id', cascade='all, delete-orphan',
        backref='users', lazy='dynamic')

    def __init__(self, username):
        ''' Initialise the user with a username '''
        self.username = username

    def password_hasher(self, password):
        ''' hashes the password '''
        self.password = Bcrypt().generate_password_hash(password)

    def password_checker(self, password):
        ''' Compare password value against the stored hashed password '''
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # header
            header = {
                'typ': 'JWT',
                'alg': 'HS256'
            }
            # payload with the claims,expiration time,subject,token issue time
            payload = {
                # expiration time, 10 minutes after current/issued time
                'exp': datetime.utcnow() + timedelta(minutes=10),
                # issued time
                'iat': datetime.utcnow(),
                # subject, user's id
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            token_string = jwt.encode(
                header, payload, current_app.config.get('SECRET_KEY'))
            return token_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET_KEY
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            # returns the user's ID
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # In case the token has expired
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # Incase the token cannot be decoded/authenticated
            return "Invalid token. Please register or login"

    def __repr__(self):
        return '<User: {}>'.format(self.username)
