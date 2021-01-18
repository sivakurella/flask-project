from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import create_access_token

from kurellaz.models.user import User
from kurellaz.utils import utils

class TokenResource(Resource):
    def post(self):
        data = request.get_json()

        # lets get username and email from request
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # either username and email was provided
        if username:
            user = User.get_by_username(username)
        elif email:
            user = User.get_by_email(email)
        else:
            return {'message':'Provide either username and email for authentication'}, HTTPStatus.BAD_REQUEST

        # now check the validity of the user and password
        if not user or not utils.check_password(password, user.password):
            return {'message': 'username or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id)

        return {'access_token': access_token}, HTTPStatus.OK
    