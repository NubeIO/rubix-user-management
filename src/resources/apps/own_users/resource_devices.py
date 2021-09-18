import shortuuid
from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.device.model_device import DeviceModel
from src.resources.utils import get_authorized_user_uuid
from src.rest_schema.schema_device import device_all_attributes, device_return_fields


class DevicesResourceList(RubixResource):
    parser = reqparse.RequestParser()
    for attr in device_all_attributes:
        parser.add_argument(attr,
                            type=device_all_attributes[attr]['type'],
                            required=device_all_attributes[attr].get('required', False),
                            help=device_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    @marshal_with(device_return_fields)
    def get(cls):
        user_uuid = get_authorized_user_uuid()
        return DeviceModel.find_all_by_user_uuid(user_uuid=user_uuid)

    @classmethod
    @marshal_with(device_return_fields)
    def post(cls):
        args = cls.parser.parse_args()
        uuid = str(shortuuid.uuid())
        user_uuid = get_authorized_user_uuid()
        device = DeviceModel.find_by_user_uuid_and_device_id(user_uuid, args['device_id'])
        if device:
            return device
        device = DeviceModel(uuid=uuid, user_uuid=user_uuid, **args)
        device.save_to_db()
        return device


class DevicesResourceByUUID(RubixResource):
    @classmethod
    @marshal_with(device_return_fields)
    def get(cls, uuid):
        user_uuid = get_authorized_user_uuid()
        device: DeviceModel = DeviceModel.find_by_user_uuid_and_uuid(user_uuid, uuid)
        if device is None:
            raise NotFoundException('Device not found')
        return device

    @classmethod
    @marshal_with(device_return_fields)
    def patch(cls, uuid):
        parser = reqparse.RequestParser()
        parser.add_argument('device_id', type=str, required=False, store_missing=False)
        parser.add_argument('device_name', type=str, required=False, store_missing=False)
        parser.add_argument('platform', type=str, required=False, store_missing=False)
        parser.add_argument('kiosk', type=bool, required=False, store_missing=False)
        args = parser.parse_args()
        user_uuid = get_authorized_user_uuid()
        device: DeviceModel = DeviceModel.find_by_user_uuid_and_uuid(user_uuid, uuid)
        if device is None:
            raise NotFoundException("Device not found")
        device.update(**args)
        return device

    @classmethod
    def delete(cls, uuid):
        user_uuid = get_authorized_user_uuid()
        device: DeviceModel = DeviceModel.find_by_user_uuid_and_uuid(user_uuid, uuid)
        if device is None:
            raise NotFoundException("Device not found")
        device.delete_from_db()
        return '', 204


class DevicesResourceByDeviceId(RubixResource):
    @classmethod
    def delete(cls, device_id):
        user_uuid = get_authorized_user_uuid()
        device: DeviceModel = DeviceModel.find_by_user_uuid_and_device_id(user_uuid, device_id)
        if device is None:
            return '', 204  # we are not throwing error even though we didn't match the device_uuid
        device.delete_from_db()
        return '', 204
