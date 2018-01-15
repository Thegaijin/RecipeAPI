''' This script handles how data is formatted and returned on get requests '''

from flask_marshmallow import Marshmallow

from app.models.category import Category
from app.models.recipe import Recipe
from app.models.user import User


ma = Marshmallow()


class UserSchema(ma.ModelSchema):
    """ User model schema """
    class Meta:
        model = User


class CategorySchema(ma.ModelSchema):
    """ Category model schema """
    class Meta:
        model = Category
    recipes = ma.Nested('RecipeSchema', many=True, load=True)


class RecipeSchema(ma.ModelSchema):
    """ Recipe model schema """
    class Meta:
        model = Recipe
