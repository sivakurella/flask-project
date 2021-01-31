from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    get_jti
)


from kurellaz.models.user import User
from kurellaz.utils import utils

# initialization for bllacklist tokens and access tokens and refresh tokens
black_list=set()
reftoken_dict={}


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

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        # add the refresh token to the dict
        reftoken_dict[get_jti(access_token)] = get_jti(refresh_token)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class RefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        #print('User_id:',current_user)

        access_token = create_access_token(identity=current_user, fresh=False)

        # add the refresh token to the dict
        reftoken_dict[get_jti(access_token)] = get_raw_jwt()['jti']

        return {'access_token': access_token}, HTTPStatus.OK
    

class RevokeResource(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        black_list.add(jti)

        # adding the refresh token to the set
        #print(reftoken_dict[jti])
        refresh_jti = reftoken_dict.get(jti)
        if refresh_jti:
            black_list.add(reftoken_dict[jti])

        return {'message': 'Successfully Logged out'}, HTTPStatus.OK