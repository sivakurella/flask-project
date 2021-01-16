from flask import Flask, jsonify, request
from http import HTTPStatus

from werkzeug.wrappers import ResponseStreamMixin


app = Flask(__name__)

recipes = [
    {'id': 1,
     'name': 'Chicken Biriyani',
     'description': 'My Favorite basmati rice recipe'
    },
    {'id': 2,
     'name': 'Pacchi Pindi Rotte',
     'description': 'My Favorite breakfast special'
    },
    {'id': 3,
     'name': 'Masala Dosa',
     'description': 'My Favorite dosa recipe'
    }
]

@app.route("/")
def say_hello():
    return "Welcome to Recipe API"

@app.route('/recipes', methods=['GET'])
def get_recipes():
    return jsonify({'recipes':recipes})

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if recipe:
        return jsonify(recipe)

    return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    print(request)
    print(data)

    name = data.get('name')
    description = data.get('description')

    recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'description': description
    }

    recipes.append(recipe)

    return jsonify(recipe), HTTPStatus.CREATED


@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if not recipe:
        return jsonify({'message':'recipe #' + str(recipe_id) +  ' not found'}), HTTPStatus.NOT_FOUND

    data = request.get_json()
    print(data)

    add_recipe={}
    name = data.get('name')
    description = data.get('description')
    if name:
        add_recipe['name'] = name
    if description:
        add_recipe['description'] = description

    recipe.update(
        add_recipe
    )

    return jsonify(recipe)

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if not recipe:
        return jsonify({'message':'recipe #' + str(recipe_id) +  " not found and can't be deleted"}), HTTPStatus.NOT_FOUND

    recipes.remove(recipe)

    return '', HTTPStatus.NO_CONTENT



if __name__ == '__main__':
    app.run()