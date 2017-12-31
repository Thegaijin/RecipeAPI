# serializers.py
''' This script has the model serializers  '''

# # Third-party import
from flask_marshmallow import Marshmallow

# Local import
from app.models.category import Category
from app.models.recipe import Recipe
from app.models.user import User


ma = Marshmallow()


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class CategorySchema(ma.ModelSchema):
    class Meta:

        model = Category


class RecipeSchema(ma.ModelSchema):
    class Meta:
        model = Recipe
