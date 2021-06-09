from flask import Blueprint
from flask_restful import Api

from src.resources.admin.resource_fcm_server import FcmServerResource
from src.resources.admin.resource_users import *
from src.resources.third_party.resource_device import DeviceResourceList, DeviceResourceByUUID
from src.resources.third_party.resource_mqtt import MqttTopicsResource, MqttConfigResource
from src.resources.third_party.resource_user import UserResource
from src.resources.third_party.resource_users import *
from src.system.resources.ping import Ping

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
bp_users = Blueprint('users', __name__, url_prefix='/api/users')
bp_fcm_server = Blueprint('fcm_server', __name__, url_prefix='/api/fcm_server')

bp_apps_users = Blueprint('apps_users', __name__, url_prefix='/api/apps/users')
bp_apps_own_users = Blueprint('apps_own_users', __name__, url_prefix='/api/apps/o/users')
bp_api_apps_configs = Blueprint('apps_configs', __name__, url_prefix='/api/apps/c')

# 1 => Admin
Api(bp_system).add_resource(Ping, '/ping')

# 2
api_users = Api(bp_users)
api_users.add_resource(UsersResourceList, '')
api_users.add_resource(UsersResourceByUUID, '/uuid/<string:uuid>')
api_users.add_resource(UsersResourceByUsername, '/username/<string:username>')
api_users.add_resource(UsersVerifyResource, '/verify')

# 3
api_apps_users = Api(bp_apps_users)
api_apps_users.add_resource(UsersCreateResource, '', endpoint="create")
api_apps_users.add_resource(UsersLoginResource, '/login', endpoint="login")
api_apps_users.add_resource(UsersChangePasswordResource, '/change_password')
api_apps_users.add_resource(UsersCheckByUsernameResource, '/check/username', endpoint='check_username')
api_apps_users.add_resource(UsersCheckByEmailResource, '/check/email', endpoint='check_email')
api_apps_users.add_resource(UsersRefreshToken, '/refresh_token')

# 4
api_apps_own_users = Api(bp_apps_own_users)
api_apps_own_users.add_resource(UserResource, '')
api_apps_own_users.add_resource(DeviceResourceList, '/devices')
api_apps_own_users.add_resource(DeviceResourceByUUID, '/devices/uuid/<string:uuid>')

# 5
api_apps_configs = Api(bp_api_apps_configs)
api_apps_configs.add_resource(MqttConfigResource, '/mqtt')
api_apps_configs.add_resource(MqttTopicsResource, '/mqtt/topics')

# 6 => Admin
api_fcm_server = Api(bp_fcm_server)
api_fcm_server.add_resource(FcmServerResource, '')
