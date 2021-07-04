from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.device.model_device import DeviceModel
from src.models.enum import StateType, FcmDataType
from src.models.fcm_server.model_fcm_server import FcmServerModel
from src.models.user.model_user import UserModel
from src.resources.utils import parse_user_update
from src.rest_schema.schema_user import user_all_fields_with_children, user_return_fields


class UsersResourceList(RubixResource):
    @classmethod
    @marshal_with(user_all_fields_with_children)
    def get(cls):
        return UserModel.find_all()


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
        data = {
            "to": "",
            "data": {
                "title": "NubeIO User Status",
                "body": "User is verified by Admin!",
                "type": FcmDataType.USER_VERIFICATION.name
            }
        }
        DeviceModel.send_notification_by_user_uuid(user.uuid, FcmServerModel.get_key(), data)
        return {'message': 'User has been verified successfully'}
