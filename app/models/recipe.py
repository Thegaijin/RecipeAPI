# app/models/recipe.py
''' This scripts holds the Category model '''

# Third party import
from datetime import datetime

# Local imports
from app import db
from app.models.crudmixin import CRUDMixin
from app.models.user import User


class Recipe(db.Model, CRUDMixin):
    ''' Class representing the recipes table '''

    __tablename__ = 'recipes'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    ingredients = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('recipes',
                                                              lazy='dynamic'))
    created_by = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User', backref=db.backref(' recipes',
                                                      lazy='dynamic'))

    def __init__(self, name, ingredients, category):
        ''' Initialise the recipe with a name and ingredients '''
        self.name = name
        self.ingredients = ingredients
        self.category = category

    def __repr__(self):
        return '<Recipe: {}>'.format(self.name)
