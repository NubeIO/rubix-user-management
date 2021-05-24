from flask_restful import marshal_with
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.user.model_user import UserModel
from src.resources.rest_schema.schema_user import user_all_fields_with_children, user_all_fields
from src.resources.utils import get_access_token, decode_jwt_token, parse_user_update


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
