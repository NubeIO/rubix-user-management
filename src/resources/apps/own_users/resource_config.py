import json

from flask import current_app
from rubix_http.resource import RubixResource

from src import AppSetting


class MqttConfigResource(RubixResource):
    @classmethod
    def get(cls):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        app_setting.mqtt.serialize()
        return json.loads(app_setting.mqtt.serialize())
