from flask import Flask, jsonify,make_response
from flask_migrate import Migrate
from flask_restful import Api
import simplejson as json

from kurellaz.config import Config

from kurellaz.extensions import db, jwt

from kurellaz.models.user import User

from kurellaz.resources.recipe import (
    RecipeListResource, 
    RecipePublishResource, 
    RecipeResource,
    MyRecipeResource)
from kurellaz.resources.user import UserResource, UserListResource, MeResource
from kurellaz.resources.token import RevokeResource, TokenResource, RefreshResource, black_list



def create_app():
    #print(__name__)
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)
    register_urls(app)

    @app.route('/api')
    def welcome():
        return jsonify({'message': 'Welcome to Recipe API'})

    return app


def register_extensions(app):
    # flask migrate extention initialization
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    # jwt extension initialization
    jwt.init_app(app)

    # check whether a token is in the blacklist
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']

        return jti in black_list


def register_resources(app):
    api = Api(app)

    # recipe resources
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
    api.add_resource(MyRecipeResource, '/myrecipes')

    # user resources
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')

    # jwt token resource
    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

    # using simplejson to deserialize the json data as default json causes errors
    # also can override the Api class too
    @api.representation('application/json')
    def output_json(data, code, headers=None):
        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})
        return resp

def register_urls(app):
    app.add_url_rule('/', 'index', index)


def index():
    return '<h1>Hello Recipe World</h1>'


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)
