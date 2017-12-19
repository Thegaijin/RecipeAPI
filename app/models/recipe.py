# app/models/recipe.py
''' This scripts holds the Category model '''

# Third party import
from datetime import datetime

# Local imports
from ..db import db
from app.models.user import User
from app.models.category import Category


class Recipe(db.Model):
    ''' Class representing the recipes table '''

    __tablename__ = 'recipes'

    # table columns
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.user_id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey(Category.category_id))

    def __init__(self, recipe_name, ingredients, category_id, created_by):
        ''' Initialise the recipe with a name, ingredients and created by '''
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.category_id = category_id
        self.created_by = created_by

    def __repr__(self):
        return '<Recipe: {}>'.format(self.recipe_name)
