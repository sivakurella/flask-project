from flask import request
from flask_restful import Resource
from http import HTTPStatus
from kurellaz.models.user import User
from kurellaz.extensions import db
from kurellaz.utils import utils

class UserResource(Resource):
    def post(self):
        data = request.get_json()

        # parse data from the request
        user = data.get('username')
        non_hash_passwd = data.get('password')
        email = data.get('email')

        # check whether the user exists
        if User.get_by_username(user):
            return {'message': f'{user} already exists, please user other username'}, HTTPStatus.BAD_REQUEST

        # check whether the email exists
        if User.get_by_email(email):
            return {'message': f'{email} already exists, please user other email address for registering'}, HTTPStatus.BAD_REQUEST

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