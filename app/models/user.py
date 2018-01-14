from flask_bcrypt import Bcrypt

from ..db import db


class User(db.Model):
    ''' Class representing the Users table '''

    __tablename__ = 'users'  # should always be plural

    # table columns
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    categories = db.relationship(
        'Category', backref='user', cascade='all, delete-orphan')
    recipes = db.relationship(
        'Recipe', backref='user', cascade='all, delete-orphan')

    def __init__(self, username, email):
        ''' Initialise the user with a username '''
        self.username = username
        self.email = email

    def password_hasher(self, password):
        ''' hashes the password '''
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

    def password_checker(self, password):
        ''' Check if hashed password and password match '''
        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)
