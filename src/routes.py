from flask import Blueprint
from flask_restful import Api

from src.resources.admin.resource_fcm_server import FcmServerResource
from src.resources.admin.resource_sites import AdminSitesResourceList, AdminSitesResourceByUUID
from src.resources.admin.resource_user_site import UserSiteResourceList, UserSiteResourceByUUID
from src.resources.admin.resource_users import *
from src.resources.apps.own_users.resource_devices import DevicesResourceList, DevicesResourceByUUID, \
    DevicesResourceByDeviceId
from src.resources.apps.own_users.resource_mqtt import MqttTopicsResource, MqttConfigResource
from src.resources.apps.own_users.resource_sites import SitesResourceList
from src.resources.apps.own_users.resource_user import UserResource
from src.resources.apps.users.resource_users import *
from src.system.resources.ping import Ping

# Admin
bp_system = Blueprint('system', __name__, url_prefix='/api/system')
bp_users_summary = Blueprint('users_summary', __name__, url_prefix='/api/users')
bp_fcm_server = Blueprint('fcm_server', __name__, url_prefix='/api/fcm_server')
bp_sites = Blueprint('sites', __name__, url_prefix='/api/sites')

# Apps
bp_users = Blueprint('users', __name__, url_prefix='/api/apps/users')
bp_own_users = Blueprint('own_users', __name__, url_prefix='/api/apps/o/users')
bp_configs = Blueprint('configs', __name__, url_prefix='/api/apps/c')

# 1 => Admin
Api(bp_system).add_resource(Ping, '/ping')

# 2 => Apps
api_users = Api(bp_users_summary)
api_users.add_resource(UsersResourceList, '')
api_users.add_resource(UsersResourceByUUID, '/uuid/<string:uuid>')
api_users.add_resource(UsersResourceByUsername, '/username/<string:username>')
api_users.add_resource(UsersVerifyResource, '/verify')
api_users.add_resource(UserSiteResourceList, '/sites')
api_users.add_resource(UserSiteResourceByUUID, '/sites/uuid/<string:uuid>')

# 3 => Apps
api_apps_users = Api(bp_users)
api_apps_users.add_resource(UsersCreateResource, '', endpoint="create")
api_apps_users.add_resource(UsersLoginResource, '/login', endpoint="login")
api_apps_users.add_resource(UsersCheckByUsernameResource, '/check/username', endpoint='check_username')
api_apps_users.add_resource(UsersCheckByEmailResource, '/check/email', endpoint='check_email')

# 4 => Apps
api_apps_own_users = Api(bp_own_users)
api_apps_own_users.add_resource(UserResource, '')
api_apps_own_users.add_resource(UsersChangePasswordResource, '/change_password')
api_apps_own_users.add_resource(UsersRefreshToken, '/refresh_token')
api_apps_own_users.add_resource(DevicesResourceList, '/devices')
api_apps_own_users.add_resource(DevicesResourceByUUID, '/devices/uuid/<string:uuid>')
api_apps_own_users.add_resource(DevicesResourceByDeviceId, '/devices/device_id/<string:device_id>')
api_apps_own_users.add_resource(SitesResourceList, '/sites')

# 5 => Apps
api_apps_configs = Api(bp_configs)
api_apps_configs.add_resource(MqttConfigResource, '/mqtt')
api_apps_configs.add_resource(MqttTopicsResource, '/mqtt/topics')

# 6 => Admin
api_fcm_server = Api(bp_fcm_server)
api_fcm_server.add_resource(FcmServerResource, '')

# 7 => Admin
api_sites = Api(bp_sites)
api_sites.add_resource(AdminSitesResourceList, '')
api_sites.add_resource(AdminSitesResourceByUUID, '/uuid/<string:uuid>')
