import shortuuid
from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.site.model_site import SiteModel
from src.rest_schema.schema_site import site_all_attributes, site_return_fields


class AdminSitesResourceList(RubixResource):
    parser = reqparse.RequestParser()
    for attr in site_all_attributes:
        parser.add_argument(attr,
                            type=site_all_attributes[attr]['type'],
                            required=site_all_attributes[attr].get('required', False),
                            help=site_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(site_return_fields)
    def get(cls):
        return SiteModel.find_all()

    @classmethod
    @marshal_with(site_return_fields)
    def post(cls):
        args = cls.parser.parse_args()
        uuid = str(shortuuid.uuid())
        site = SiteModel(uuid=uuid, **args)
        site.save_to_db()
        return site


class AdminSitesResourceByUUID(RubixResource):
    patch_parser = reqparse.RequestParser()
    for attr in site_all_attributes:
        patch_parser.add_argument(attr,
                                  type=site_all_attributes[attr]['type'],
                                  required=False,
                                  help=site_all_attributes[attr].get('help', None),
                                  store_missing=False)

    @classmethod
    @marshal_with(site_return_fields)
    def get(cls, uuid):
        site: SiteModel = SiteModel.find_by_uuid(uuid)
        if site is None:
            raise NotFoundException('Site not found')
        return site

    @classmethod
    @marshal_with(site_return_fields)
    def patch(cls, uuid):
        args = AdminSitesResourceByUUID.patch_parser.parse_args()
        site: SiteModel = SiteModel.find_by_uuid(uuid)
        if site is None:
            raise NotFoundException("Site not found")
        site.update(**args)
        return site

    @classmethod
    def delete(cls, uuid):
        site: SiteModel = SiteModel.find_by_uuid(uuid)
        if site is None:
            raise NotFoundException("Site not found")
        site.delete_from_db()
        return '', 204
