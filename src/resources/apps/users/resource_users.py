import shortuuid
from flask_restful import reqparse
from rubix_http.exceptions.exception import NotFoundException, UnauthorizedException, BadDataException
from rubix_http.resource import RubixResource
from werkzeug.security import check_password_hash

from src.models.user.model_user import UserModel
from src.resources.utils import encrypt_password, encode_jwt_token, get_authorized_user_uuid, get_authorized_username
from src.rest_schema.schema_user import user_all_attributes


class UsersCreateResource(RubixResource):
    parser = reqparse.RequestParser()
    for attr in user_all_attributes:
        parser.add_argument(attr,
                            type=user_all_attributes[attr]['type'],
                            required=user_all_attributes[attr].get('required', False),
                            help=user_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def post(cls):
        args = cls.parser.parse_args()
        uuid_ = str(shortuuid.uuid())
        user = UserModel(uuid=uuid_, **args)
        user.password = encrypt_password(user.password)
        user.save_to_db()
        return encode_jwt_token(user.uuid, user.username)


class UsersChangePasswordResource(RubixResource):

    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, store_missing=False)
        parser.add_argument('password', type=str, required=True, store_missing=False)
        parser.add_argument('new_password', type=str, required=True, store_missing=False)
        args = parser.parse_args()
        username = get_authorized_username()
        user: UserModel = UserModel.find_by_username(username)
        if user is None:
            raise NotFoundException("User does not exist")
        if not (args['username'] == username and check_password_hash(user.password, args['password'])):
            raise UnauthorizedException("Invalid username or password")
        user.password = encrypt_password(args['new_password'])
        user.commit()
        return {'message': 'Your password has been changed successfully'}


class UsersLoginResource(RubixResource):
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


class UsersCheckByUsernameResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, store_missing=False)
        args = parser.parse_args()
        user: UserModel = UserModel.find_by_username(args['username'])
        return {'exist': bool(user)}


class UsersCheckByEmailResource(RubixResource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, store_missing=False)
        args = parser.parse_args()
        user: UserModel = UserModel.find_by_email(args['email'])
        return {'exist': bool(user)}


class UsersRefreshToken(RubixResource):
    @classmethod
    def get(cls):
        username = get_authorized_username()
        uuid_ = get_authorized_user_uuid()
        return encode_jwt_token(uuid_, username)
