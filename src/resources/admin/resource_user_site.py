import uuid as uuid_

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.user_site.model_user_site import UserSiteModel
from src.rest_schema.schema_user_site import user_site_all_attributes, user_site_return_fields


class UserSiteResourceList(RubixResource):
    parser = reqparse.RequestParser()
    for attr in user_site_all_attributes:
        parser.add_argument(attr,
                            type=user_site_all_attributes[attr]['type'],
                            required=user_site_all_attributes[attr].get('required', False),
                            help=user_site_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(user_site_return_fields)
    def get(cls):
        return UserSiteModel.find_all()

    @classmethod
    @marshal_with(user_site_return_fields)
    def post(cls):
        args = cls.parser.parse_args()
        uuid = str(uuid_.uuid4())
        user_site = UserSiteModel(uuid=uuid, **args)
        user_site.save_to_db()
        return user_site


class UserSiteResourceByUUID(RubixResource):
    @classmethod
    @marshal_with(user_site_return_fields)
    def get(cls, uuid):
        user_site: UserSiteModel = UserSiteModel.find_by_uuid(uuid)
        if user_site is None:
            raise NotFoundException("Given UUID doesn't exist on users_sites relation")
        return user_site

    @classmethod
    def delete(cls, uuid):
        user_site: UserSiteModel = UserSiteModel.find_by_uuid(uuid)
        if user_site is None:
            raise NotFoundException("Given UUID doesn't exist on users_sites relation")
        user_site.delete_from_db()
        return '', 204
