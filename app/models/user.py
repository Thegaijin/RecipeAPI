# app/models/user.py
''' This scripts holds the DB table models '''


# Local import
from ..db import db


class User(db.Model):
    ''' Class representing the Users table '''

    __tablename__ = 'users'  # should always be plural

    # table columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    # categories = db.relationship('Category', cascade='all, delete-orphan',
    # backref='users', lazy='dynamic')

    def __init__(self, username, password):
        ''' Initialise the user with a username '''
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User: {}>'.format(self.username)
