from flask_restful import marshal_with
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.user.model_user import UserModel
from src.resources.utils import parse_user_update, get_authorized_user_uuid
from src.rest_schema.schema_user import user_all_fields, user_all_fields_with_children


class UserResource(RubixResource):

    @classmethod
    @marshal_with(user_all_fields_with_children)
    def get(cls):
        uuid = get_authorized_user_uuid()
        user = UserModel.find_by_uuid(uuid)
        if not user:
            raise NotFoundException("User does not exist")
        return user

    @classmethod
    @marshal_with(user_all_fields)
    def patch(cls):
        uuid = get_authorized_user_uuid()
        user = UserModel.find_by_uuid(uuid)
        if not user:
            raise NotFoundException("User does not exist")
        args = parse_user_update()
        user.update(**args)
        return user

    @classmethod
    def delete(cls):
        uuid = get_authorized_user_uuid()
        user = UserModel.find_by_uuid(uuid)
        if user is None:
            raise NotFoundException("User does not exist")
        user.delete_from_db()
        return '', 204
