from typing import List

from flask_restful import marshal_with
from rubix_http.resource import RubixResource, NotFoundException

from src.models.site.model_site import SiteModel
from src.models.user.model_user import UserModel
from src.resources.utils import get_authorized_user_uuid
from src.rest_schema.schema_site import site_return_fields


class SitesResourceList(RubixResource):

    @classmethod
    @marshal_with(site_return_fields)
    def get(cls):
        uuid = get_authorized_user_uuid()
        user = UserModel.find_by_uuid(uuid)
        if not user:
            raise NotFoundException("User does not exist")
        output: List[SiteModel] = []
        for site in user.sites:
            output.append(SiteModel.find_by_uuid(site.site_uuid))
        return output
