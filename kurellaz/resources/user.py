from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from marshmallow import ValidationError

from kurellaz.schemas.user import UserSchema
from kurellaz.models.user import User
from kurellaz.extensions import db
from kurellaz.utils import utils

user_schema  = UserSchema()
user_public_schema = UserSchema(exclude=('email',))

class UserListResource(Resource):
    def post(self):
        data = request.get_json()

        # lets load the data into the user schema
        try:
            user_data = user_schema.load(data=data)
        except ValidationError as verr  :
            return {'message': 'Validation Errors', 'errors':verr.messages}, HTTPStatus.BAD_REQUEST

        # parse data from the request
        user = user_data.get('username')
        non_hash_passwd = data.get('password')
        email = user_data.get('email')

        # check whether the user exists
        if User.get_by_username(user):
            return {'message': f'{user} already exists, please use other username'}, HTTPStatus.BAD_REQUEST

        # check whether the email exists
        if User.get_by_email(email):
            return {'message': f'{email} already exists, please use other email address for registering'}, HTTPStatus.BAD_REQUEST

        # check the length of the password
        if len(non_hash_passwd) < 4:
            return {'message': 'Length of the password has to >= 4'}, HTTPStatus.BAD_REQUEST

        # hash the user password
        # hashed_password = utils.hash_password(non_hash_passwd)

        user = User(
            **user_data
            # username = user,
            # email = email,
            # password = hashed_password
        )

        # save the user and commit
        user.save()

        return user_schema.dump(user), HTTPStatus.CREATED
    
class UserResource(Resource):
    @jwt_optional
    def get(self, username):
        
        # get user by username
        user = User.get_by_username(username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user)
            # {
            #     'id': user.id,
            #     'email': user.email,
            #     'username': user.username
            # }
        else:
             data = user_public_schema.dump(user)
            #  {
            #     'id': user.id,
            #     'username': user.username
            # }

        return data, HTTPStatus.OK

class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id = get_jwt_identity())

        data = user_schema.dump(user)
        #  {
        #     "id": user.id,
        #     "username": user.username,
        #     "email": user.email
        # }

        return data, HTTPStatus.OK

