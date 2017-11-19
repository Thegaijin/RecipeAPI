# app/models.py
''' This scripts holds the DB table models '''

# Third party import
from flask_bcrypt import Bcrypt

# Local import
from app import db


class User(db.Model):
    ''' Class representing the Users table '''

    __tablename__ = 'users'  # should always be plural

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    categories = db.relationship(
        'Category', order_by='category.id', cascade='all, delete-orphan',
        backref='users', lazy='dynamic')

    def __init__(self, username, password):
        ''' Initialise the user with a username and password '''
        self.username = username
        # hashing password value
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_authentication(self, password):
        """ Compare passed password value against the stored hashed password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Category(db.Model):
    ''' Class representing the categories table '''

    __tablename__ = 'categories'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    recipes = db.relationship(
        'Recipe', order_by='recipe.id', cascade='all, delete-orphan',
        backref='categories')

    def __init__(self, name, description):
        ''' Initialise the category with a name and description '''

        self.name = name
        self.description = description

    def __repr__(self):
        return '<Category: {}>'.format(self.name)


class Recipe(db.Model):
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

    def __init__(self, name, ingredients):
        ''' Initialise the recipe with a name and ingredients '''
        self.name = name
        self.ingredients = ingredients

    def __repr__(self):
        return '<Recipe: {}>'.format(self.name)
