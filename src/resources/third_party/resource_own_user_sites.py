from flask_restful import marshal_with
from rubix_http.resource import RubixResource, NotFoundException

from src.models.user.model_user import UserModel
from src.resources.utils import get_access_token, decode_jwt_token
from src.rest_schema.schema_site import site_return_fields


class OwnUserSitesResourceList(RubixResource):

    @classmethod
    @marshal_with(site_return_fields)
    def get(cls):
        access_token = get_access_token()
        uuid = decode_jwt_token(access_token).get('sub', '')
        user = UserModel.find_by_uuid(uuid)
        if not user:
            raise NotFoundException("User does not exist")
        return user.sites
