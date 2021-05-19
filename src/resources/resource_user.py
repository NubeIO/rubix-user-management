from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException, BadDataException
from rubix_http.resource import RubixResource
from werkzeug.security import check_password_hash

from src.models.user.model_user import UserModel
from src.resources.rest_schema.schema_user import user_all_fields_with_children, user_all_fields
from src.resources.utils import get_access_token, decode_jwt_token, parse_user_update, encrypt_password, \
    encode_jwt_token


class UserChangePasswordResource(RubixResource):

    @classmethod
    def post(cls):
        access_token = get_access_token()
        parser = reqparse.RequestParser()
        parser.add_argument('new_password', type=str, required=True, store_missing=False)
        args = parser.parse_args()
        username = decode_jwt_token(access_token).get('username', '')
        user: UserModel = UserModel.find_by_username(username)
        if user is None:
            raise NotFoundException("User does not exist")
        user.password = encrypt_password(args['new_password'])
        user.commit()
        return {'message': 'Your password has been changed successfully'}


class UserLoginResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, store_missing=False)
        parser.add_argument('password', type=str, required=True, store_missing=False)
        args = parser.parse_args()
        user = UserModel.find_by_username(args['username'])
        if user is None:
            raise NotFoundException('User does not exist')
        if not check_password_hash(user.password, args['password']):
            raise BadDataException('username and password combination is incorrect')
        return encode_jwt_token(user.uuid, user.username)


class UserResource(RubixResource):

    @classmethod
    @marshal_with(user_all_fields_with_children)
    def get(cls):
        access_token = get_access_token()
        uuid = decode_jwt_token(access_token).get('sub', '')
        user = UserModel.find_by_uuid(uuid)
        if not user:
            raise NotFoundException("User does not exist")
        return user

    @classmethod
    @marshal_with(user_all_fields)
    def patch(cls):
        access_token = get_access_token()
        uuid = decode_jwt_token(access_token).get('sub', '')
        user = UserModel.find_by_uuid(uuid)
        if not user:
            raise NotFoundException("User does not exist")
        args = parse_user_update()
        user.update(**args)
        return user

    @classmethod
    def delete(cls):
        access_token = get_access_token()
        uuid = decode_jwt_token(access_token).get('sub', '')
        user = UserModel.find_by_uuid(uuid)
        if user is None:
            raise NotFoundException("User does not exist")
        user.delete_from_db()
        return '', 204


class UserAuthenticateResource(RubixResource):
    @classmethod
    def get(cls):
        access_token = get_access_token()
        username = decode_jwt_token(access_token).get('username', '')
        uuid = decode_jwt_token(access_token).get('sub', '')
        user: UserModel = UserModel.find_by_uuid(uuid)
        if user is None:
            raise NotFoundException("User does not exist")
        return {'username': username, 'state': user.state.value}
