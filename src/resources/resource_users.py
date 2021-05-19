import uuid as uuid_
from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.enum import StateType
from src.models.user.model_user import UserModel
from src.resources.rest_schema.schema_user import user_all_attributes, user_return_fields, user_all_fields_with_children
from src.resources.utils import encrypt_password, parse_user_update, encode_jwt_token


class UsersResourceList(RubixResource):
    parser = reqparse.RequestParser()
    for attr in user_all_attributes:
        parser.add_argument(attr,
                            type=user_all_attributes[attr]['type'],
                            required=user_all_attributes[attr].get('required', False),
                            help=user_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(user_all_fields_with_children)
    def get(cls):
        return UserModel.find_all()

    @classmethod
    def post(cls):
        args = cls.parser.parse_args()
        uuid = str(uuid_.uuid4())
        user = UserModel(uuid=uuid, **args)
        user.password = encrypt_password(user.password)
        user.save_to_db()
        return encode_jwt_token(user.uuid, user.username)


class UsersResource(RubixResource):
    @classmethod
    @marshal_with(user_all_fields_with_children)
    def get(cls, **kwargs):
        user: UserModel = cls.get_user(**kwargs)
        if user is None:
            raise NotFoundException('User does not exist')
        return user

    @classmethod
    @marshal_with(user_return_fields)
    def patch(cls, **kwargs):
        args = parse_user_update()
        user: UserModel = cls.get_user(**kwargs)
        if user is None:
            raise NotFoundException("User does not exist")
        user.update(**args)
        return user

    @classmethod
    def delete(cls, **kwargs):
        user: UserModel = cls.get_user(**kwargs)
        if user is None:
            raise NotFoundException("User does not exist")
        user.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_user(cls, **kwargs) -> UserModel:
        raise NotImplementedError


class UsersResourceByUUID(UsersResource):
    @classmethod
    @abstractmethod
    def get_user(cls, **kwargs) -> UserModel:
        return UserModel.find_by_uuid(kwargs.get('uuid'))


class UsersResourceByUsername(UsersResource):
    @classmethod
    @abstractmethod
    def get_user(cls, **kwargs) -> UserModel:
        return UserModel.find_by_username(kwargs.get('username'))


class UsersVerifyResource(RubixResource):

    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, store_missing=False)
        args = parser.parse_args()
        user: UserModel = UserModel.find_by_username(args['username'])
        if user is None:
            raise NotFoundException("User does not exist")
        user.state = StateType.VERIFIED
        user.commit()
        return {'message': 'User has been verified successfully'}
