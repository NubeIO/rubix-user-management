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


class UserSiteResourceByUserUUID(RubixResource):
    @classmethod
    @marshal_with(user_site_return_fields)
    def get(cls, user_uuid):
        user_site: UserSiteModel = UserSiteModel.find_by_user_uuid(user_uuid)
        if user_site is None:
            raise NotFoundException('User site not found')
        return user_site


class UserSiteResourceByUUID(RubixResource):
    @classmethod
    @marshal_with(user_site_return_fields)
    def get(cls, uuid):
        user_site: UserSiteModel = UserSiteModel.find_by_uuid(uuid)
        if user_site is None:
            raise NotFoundException('User site not found')
        return user_site

    @classmethod
    @marshal_with(user_site_return_fields)
    def patch(cls, uuid):
        parser = reqparse.RequestParser()
        parser.add_argument('site_uuid', type=str, required=False, store_missing=False)
        args = parser.parse_args()
        user_site: UserSiteModel = UserSiteModel.find_by_uuid(uuid)
        if user_site is None:
            raise NotFoundException("User site not found")
        user_site.update(**args)
        return user_site

    @classmethod
    def delete(cls, uuid):
        user_site: UserSiteModel = UserSiteModel.find_by_uuid(uuid)
        if user_site is None:
            raise NotFoundException("User site not found")
        user_site.delete_from_db()
        return '', 204
