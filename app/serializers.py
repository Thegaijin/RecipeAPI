# # serializers.py
# ''' This script has the model serializers  '''

# # Third-party imports
# from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, pre_load, validate

# Local import
# from app import marsw
from app.models.category import Category
from app.models.recipe import Recipe
from app.models.user import User


ma = Marshmallow()

# # Custom validator


# def must_not_be_blank(data):
#     if not data:
#         raise ValidationError('Data not provided.')


# class UserSchema(ma.Schema):
#     user_id = fields.Integer(dump_only=True, validate=must_not_be_blank)
#     password = fields.String(required=True, validate=must_not_be_blank)


# class CategorySchema(ma.Schema):
#     category_id = fields.Int(dump_only=True)
#     category_name = fields.Str(required=True, validate=must_not_be_blank)
#     description = fields.Str(required=True, validate=must_not_be_blank)
#     created_by = fields.Int(dump_only=True)

#     @pre_load
#     def process_category(self, data):
#         """method to process the category data

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class CategorySchema(ma.ModelSchema):
    class Meta:

        model = Category


class RecipeSchema(ma.ModelSchema):
    class Meta:
        model = Recipe
