import re
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from kurellaz.models.recipe import Recipe
from kurellaz.extensions import db
from flask_jwt_extended import (
    jwt_optional,
    jwt_required, 
    get_jwt_identity)
from marshmallow import ValidationError
from kurellaz.schemas.recipe import RecipeSchema

recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)

class RecipeListResource(Resource):
    def get(self):
        # data = []
        # for recipe in Recipe.get_all_published():
        #     data.append(recipe.data)
        recipes = Recipe.get_all_published()

        return recipe_list_schema.dump(recipes), HTTPStatus.OK

    @jwt_required
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()

        # load the request data into the recipe schema
        try:
            user_recipe = recipe_schema.load(data=data)
        except ValidationError as verr  :
            return {'message': 'Validation Errors',\
                 'errors':verr.messages,
                 'RecipeSchema': [field for field in recipe_schema.declared_fields \
                     if not recipe_schema.declared_fields[field].dump_only]}\
                     , HTTPStatus.BAD_REQUEST

        recipe = Recipe(
            **user_recipe
        )
        recipe.user_id = current_user

        recipe.save()

        # get the recipe after saving
        saved_recipe = Recipe.get_by_id(recipe_id = recipe.id)

        return recipe_schema.dump(saved_recipe), HTTPStatus.CREATED

class MyRecipeResource(Resource):
    @jwt_required
    def get(self):
        data = []

        # get the user identity
        current_user = get_jwt_identity()

        # get all the recipes of the userid
        for recipe in Recipe.get_by_userid(user_id=current_user):
                data.append(recipe)

        try:
            json_data = recipe_list_schema.dump(data)
        except:
            return {'message': 'Kaboom something is messed up'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
        return json_data, HTTPStatus.OK


class RecipeResource(Resource):
    @jwt_optional
    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if not recipe:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        
        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message': 'Access is not Allowed'}, HTTPStatus.FORBIDDEN

        try:
            json_data = recipe_schema.dump(recipe)
        except:
            return {'message': 'Kaboom something is messed up'}, HTTPStatus.INTERNAL_SERVER_ERROR

        return json_data, HTTPStatus.OK

    @jwt_required
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if not recipe:
            return {'message':'recipe #' + str(recipe_id) +  ' not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not Allowed'}, HTTPStatus.FORBIDDEN

        data = request.get_json()

        # parse data from the request
        name = data.get('name')
        description = data.get('description')
        num_of_servings = data.get('num_of_servings')
        cook_time = data.get('cook_time')
        directions = data.get('directions')

        if name:
            recipe.name = name
        if description:
            recipe.description = description
        
        # update the rest of the attributes
        recipe.num_of_servings = num_of_servings
        recipe.cook_time = cook_time
        recipe.directions  = directions

        recipe.save()

        return recipe.data, HTTPStatus.OK

    @jwt_required
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if not recipe:
            return {'message':'recipe #' + str(recipe_id) +  ' not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not Allowed'}, HTTPStatus.FORBIDDEN

        recipe.delete()

        return {}, HTTPStatus.NO_CONTENT

class RecipePublishResource(Resource):
    @jwt_required
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not Allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = True

        recipe.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not Allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = False

        recipe.save()

        return {}, HTTPStatus.NO_CONTENT