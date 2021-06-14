from registry.registry import RubixRegistry
from rubix_http.resource import RubixResource

from src.models.user.model_user import UserModel
from src.resources.utils import get_access_token, decode_jwt_token


class MqttTopicsResource(RubixResource):
    @classmethod
    def get(cls):
        global_uuid: str = RubixRegistry().read_wires_plat().get("global_uuid")
        access_token = get_access_token()
        uuid = decode_jwt_token(access_token).get('sub', '')
        user = UserModel.find_by_uuid(uuid)
        output: dict = {}
        for site in user.sites:
            output[site.uuid] = {
                'layout_topic': f'{global_uuid}/{site.uuid}/layout',
                'alert_topic': f'{global_uuid}/{site.uuid}/alerts'
            }
        return output
