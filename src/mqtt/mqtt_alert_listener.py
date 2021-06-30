import json
import logging
from typing import Union, List, Callable

import gevent
from flask import current_app
from flask.ctx import AppContext
from paho.mqtt.client import MQTTMessage
from registry.registry import RubixRegistry
from rubix_mqtt.mqtt import MqttClientBase

from src.handlers.exception import exception_handler
from src.setting import MqttSetting

logger = logging.getLogger(__name__)


class MqttAlertListener(MqttClientBase):
    SEPARATOR: str = '/'

    def __init__(self):
        self.__config: Union[MqttSetting, None] = None
        self.__app_context: Union[AppContext, None] = None
        MqttClientBase.__init__(self)

    @property
    def config(self):
        return self.__config

    def start(self, config: MqttSetting, subscribe_topics: List[str] = None, callback: Callable = lambda: None):
        self.__app_context: Union[AppContext] = current_app.app_context
        self.__config = config
        subscribe_topics: List[str] = [self.make_topic()]

        super().start(config, subscribe_topics, callback)

    @exception_handler
    def _on_message(self, client, userdata, message: MQTTMessage):
        logger.debug(f'Listener Topic: {message.topic}, Message: {message.payload}')
        with self.__app_context():
            alerts = json.loads(message.payload).get('alerts', [])
            if len(alerts) == 0:
                return
            topic_parts = message.topic.split(self.SEPARATOR)
            if len(topic_parts) == len(self.make_topic().split(self.SEPARATOR)):
                site_uuid: str = topic_parts[1]
                from src.models.user_site.model_user_site import UserSiteModel
                site_users = UserSiteModel.find_by_site_uuid(site_uuid)
                for user in site_users:
                    for alert in alerts:
                        title = alert.get("title")
                        subtitle = alert.get("subtitle")
                        if title and subtitle:
                            data = {
                                "to": "",
                                "data": {
                                    "title": title,
                                    "body": subtitle
                                }
                            }
                            gevent.spawn(self.send_notification(user.user_uuid, data, self.__app_context))

    @classmethod
    def send_notification(cls, user_uuid: str, data: dict, app_context):
        with app_context():
            from src.models.device.model_device import DeviceModel
            from src.models.fcm_server.model_fcm_server import FcmServerModel
            DeviceModel.send_notification_by_user_uuid(user_uuid, FcmServerModel.get_key(), data)

    @classmethod
    def make_topic(cls) -> str:
        global_uuid: str = RubixRegistry().read_wires_plat().get("global_uuid")
        return f'{global_uuid}/+/alerts'
