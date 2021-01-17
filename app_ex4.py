from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from kurellaz.config import Config
from kurellaz.extensions import db
from kurellaz.models.user import User
from kurellaz.resources.recipe import RecipeListResource, RecipePublishResource, RecipeResource
from kurellaz.resources.user import UserResource


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
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    api = Api(app)
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
    api.add_resource(UserResource, '/users')


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)