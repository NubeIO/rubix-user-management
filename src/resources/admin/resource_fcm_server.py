import shortuuid

from flask_restful import reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.fcm_server.model_fcm_server import FcmServerModel
from src.resources.utils import aes_encrypt
from src.rest_schema.schema_fcm_server import fcm_server_all_attributes


class FcmServerResource(RubixResource):
    parser = reqparse.RequestParser()
    for attr in fcm_server_all_attributes:
        parser.add_argument(attr,
                            type=fcm_server_all_attributes[attr]['type'],
                            required=fcm_server_all_attributes[attr].get('required', False),
                            help=fcm_server_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def get(cls):
        key = FcmServerModel.get_key()
        if not key:
            raise NotFoundException("Fcm server does not exist")
        return {"key": f"***{key[-4:]}"}

    @classmethod
    def put(cls):
        args = cls.parser.parse_args()
        args['key'] = aes_encrypt(args['key'])
        fcm_server = FcmServerModel.find_one()
        if not fcm_server:
            uuid = str(shortuuid.uuid())
            fcm_server = FcmServerModel(uuid=uuid, **args)
            fcm_server.save_to_db()
        else:
            fcm_server.update(**args)
        return {"message": "Fcm server has been saved successfully"}
