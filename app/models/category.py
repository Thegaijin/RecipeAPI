# app/models/category.py
''' This scripts holds the Category model '''

# Third party import
from datetime import datetime

# Local import
from app.models.user import User
from ..db import db


class Category(db.Model):
    ''' Class representing the categories table '''

    __tablename__ = 'categories'

    # table columns
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.user_id))
    recipes = db.relationship('Recipe', cascade='all, delete-orphan')

    def __init__(self, category_name, description, created_by):
        ''' Initialise the category with a name, description and created by '''

        self.category_name = category_name
        self.description = description
        self.created_by = created_by

    def __repr__(self):
        ''' Tells python how to print the objects from the class '''
        return '<Category: {}>'.format(self.category_name)
