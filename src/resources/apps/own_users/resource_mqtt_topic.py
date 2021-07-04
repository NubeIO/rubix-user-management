import logging
from typing import Union

from registry.models.model_device_info import DeviceInfoModel
from registry.resources.resource_device_info import get_device_info
from rubix_http.resource import RubixResource

from src.models.user.model_user import UserModel
from src.resources.utils import get_authorized_user_uuid

logger = logging.getLogger(__name__)


class MqttTopicsResource(RubixResource):
    @classmethod
    def get(cls):
        device_info: Union[DeviceInfoModel, None] = get_device_info()
        if not device_info:
            logger.error('Please add device_info on Rubix Service')
            return
        uuid = get_authorized_user_uuid()
        user = UserModel.find_by_uuid(uuid)
        output: dict = {}
        for site in user.sites:
            output[site.site_uuid] = {
                'layout_topic': f'{device_info.global_uuid}/{site.site_uuid}/layout',
                'alert_topic': f'{device_info.global_uuid}/{site.site_uuid}/alerts'
            }
        return output
