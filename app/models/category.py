# app/models/category.py
''' This scripts holds the Category model '''

# Third party import
from datetime import datetime

# Local import
from app import db
from app.models.user import User


class Category(db.Model):
    ''' Class representing the categories table '''

    __tablename__ = 'categories'

    # table columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    # user = db.relationship('User', backref=db.backref(' categories',
    # lazy = 'dynamic'))
    recipes = db.relationship('Recipe', cascade='all, delete-orphan',
                              backref='categories')

    def __init__(self, name, description):
        ''' Initialise the category with a name and description '''

        self.name = name
        self.description = description

    def __repr__(self):
        ''' Tells python how to print the objects from the class '''
        return '<Category: {}>'.format(self.name)
