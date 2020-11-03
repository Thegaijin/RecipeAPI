# get_helper.py
''' This script handles pagination of recipe get request data '''

from flask import jsonify

from .serializers import RecipeSchema
THE_PAGE = 1
PER_PAGE_MIN = 5
PER_PAGE_MAX = 10


def manage_get_recipes(the_recipes, args):
    """ Function to handle search and pagination
        It receives a BaseQuery object of recipes, checks if the search
        parameter was passed a value and searches for that value.
        If the pagination parameters were passed values, checks if they are
        within the min/max range per page and paginates accordingly.

        :param object the_recipes: -- [description]
        :param list args: -- [description]
        :return:
    """

    q = args.get('q', '')
    page = args.get('page', THE_PAGE)
    per_page = args.get('per_page', PER_PAGE_MAX)
    if per_page is None or per_page < PER_PAGE_MIN:
        per_page = PER_PAGE_MIN
    if per_page > PER_PAGE_MAX:
        per_page = PER_PAGE_MAX

    for a_recipe in the_recipes.all():
        if q:
            q = q.lower()
            if q in a_recipe.recipe_name:
                recipeschema = RecipeSchema()
                the_recipe = recipeschema.dump(a_recipe)
                return jsonify(the_recipe.data)

    pag_recipes = the_recipes.paginate(
        page, per_page, error_out=False)

    pages = pag_recipes.pages
    page = pag_recipes.page
    categoryId = 0
    if not pag_recipes.items:
        return {'message': f'There are no recipes on page {page}'}
    paginated = []
    for a_recipe in pag_recipes.items:
        paginated.append(a_recipe)
    recipesschema = RecipeSchema(many=True)
    all_recipes = recipesschema.dump(paginated)

    response = {"recipes": all_recipes.data,
                "message": "These are the recipes",
                "recipePages": pages,
                "recipePage": page,
                "categoryId": categoryId,
                }
    # print("the recipe response", response)
    return response


def manage_get_recipe(the_recipe):
    recipeschema = RecipeSchema()
    get_response = recipeschema.dump(the_recipe)
    return jsonify(get_response.data)
