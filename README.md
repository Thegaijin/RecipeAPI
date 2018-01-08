[![Build Status](https://travis-ci.org/Thegaijin/RecipeAPI.svg?branch=master)](https://travis-ci.org/Thegaijin/RecipeAPI)
[![Coverage Status](https://coveralls.io/repos/github/Thegaijin/RecipeAPI/badge.svg?branch=validate)](https://coveralls.io/github/Thegaijin/RecipeAPI?branch=validate)
<a href="https://www.python.org/dev/peps/pep-0008/">
<img class="notice-badge" src="https://img.shields.io/badge/code%20style-pep8-orange.svg" alt="Badge"/>
</a>
<a href="https://codeclimate.com/github/Thegaijin/RecipeAPI/maintainability"><img src="https://api.codeclimate.com/v1/badges/c75e4a167e39a25c50aa/maintainability" /></a>

# RecipeAPI

This is an API for an Recipes service using Flask. Users can register an account and login to create, edit, view and delete recipes.

Add link to Heroku here

| EndPoint                                   | Functionality                                    |
| ------------------------------------------ | ------------------------------------------------ |
| [ POST /auth/login/ ](#)                   | Logs a user in                                   |
| [ POST /auth/register/ ](#)                | Register a user                                  |
| [ DELETE /auth/logout/ ](#)                | Logout a user                                    |
| [ POST /categories/ ](#)                   | Create a new category                            |
| [ GET /categories/ ](#)                    | Get all categories created by the logged in user |
| [ GET /categories/\<id>/ ](#)              | Get a category by it's id                        |
| [ PUT /categories/\<id>/ ](#)              | Update the category                              |
| [ DELETE /categories/\<id>/ ](#)           | Delete the category                              |
| [ POST /recipes/\<id>/ ](#)                | Create a recipe in the specified category        |
| [ GET /recipes/](#)                        | Get all recipes created by the logged in user    |
| [ GET /recipes/\<id>/](#)                  | Get all recipes in the specified category id     |
| [ GET /recipes/\<id>/\<recipe_name>](#)    | Get a recipe in the specified category id        |
| [ PUT /recipes/\<id>/<recipe_name> ](#)    | Update the recipe in the specified category id   |
| [ DELETE /recipes/\<id>/<recipe_name> ](#) | Delete the recipe in the specified category id   |

## Setup

To use the application, ensure that you have python 3.6+, clone the repository to your local machine. Open your git commandline and run

1. Clone the repository

   git clone https://github.com/Thegaijin/recipeAPI.git

2. Enter the project directory

   cd recipeAPI

3. Create a virtual environment

   virtualenv venv

4. Activate the virtual environment

   source venv/bin/activate

5. Then install all the required dependencies:

   pip install -r requirements.txt

6. Setup your postgres database using the config file provided.

7. Create the Databases

```
###Test Database
createdb test_db;

###Development Database
createdb recipe_db;
```

8. Run Migrations using these commands, in that order:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

9. To test the application, run the command :

```
pytest --cov-report term --cov=app
```

10. To start the server, run the command:

    python manage.py runserver
