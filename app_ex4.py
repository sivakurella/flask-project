from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api

from kurellaz.config import Config

from kurellaz.extensions import db, jwt

from kurellaz.models.user import User

from kurellaz.resources.recipe import RecipeListResource, RecipePublishResource, RecipeResource
from kurellaz.resources.user import UserResource, UserListResource
from kurellaz.resources.token import TokenResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    @app.route('/')
    def welcome():
        return jsonify({'message': 'Welcome to Recipe API'})

    return app


def register_extensions(app):
    # flask migrate extention initialization
    db.init_app(app)
    migrate = Migrate(app, db)

    # jwt extension initialization
    jwt.init_app(app)


def register_resources(app):
    api = Api(app)

    # recipe resources
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')

    # user resources
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')

    # jwt token resource
    api.add_resource(TokenResource, '/token')


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)
