import json

from flask import current_app
from registry.registry import RubixRegistry
from rubix_http.resource import RubixResource

from src import AppSetting


class MqttConfigResource(RubixResource):
    @classmethod
    def get(cls):
        app_setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        app_setting.mqtt.serialize()
        return json.loads(app_setting.mqtt.serialize())


class MqttTopicsResource(RubixResource):
    @classmethod
    def get(cls):
        global_uuid: str = RubixRegistry().read_wires_plat().get("global_uuid")
        return {
            "layout_topic": f'{global_uuid}/layout',
            "alert_topic": f'{global_uuid}/alerts'
        }
