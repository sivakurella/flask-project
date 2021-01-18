from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_optional, get_jwt_identity

from kurellaz.models.user import User
from kurellaz.extensions import db
from kurellaz.utils import utils

class UserListResource(Resource):
    def post(self):
        data = request.get_json()

        # parse data from the request
        user = data.get('username')
        non_hash_passwd = data.get('password')
        email = data.get('email')

        # check whether the user exists
        if User.get_by_username(user):
            return {'message': f'{user} already exists, please use other username'}, HTTPStatus.BAD_REQUEST

        # check whether the email exists
        if User.get_by_email(email):
            return {'message': f'{email} already exists, please use other email address for registering'}, HTTPStatus.BAD_REQUEST

        # hash the user password
        hashed_password = utils.hash_password(non_hash_passwd)

        user = User(
            username = user,
            email = email,
            password = hashed_password
        )

        # save the user and commit
        user.save()

        return user.data, HTTPStatus.CREATED
    
class UserResource(Resource):
    @jwt_optional
    def get(self, username):
        
        # get user by username
        user = User.get_by_username(username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        else:
            data = {
                'id': user.id,
                'username': user.username
            }

        return data, HTTPStatus.OK

