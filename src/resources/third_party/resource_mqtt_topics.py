from registry.registry import RubixRegistry
from rubix_http.resource import RubixResource


class MqttTopicsResource(RubixResource):
    @classmethod
    def get(cls):
        global_uuid: str = RubixRegistry().read_wires_plat().get("global_uuid")
        return {
            "layout_topic": f'{global_uuid}/layout',
            "alert_topic": f'{global_uuid}/alerts'
        }
