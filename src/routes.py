from flask import Blueprint
from flask_restful import Api

from src.resources.resource_current_user import CurrentUserResource
from src.resources.resource_device import DeviceResourceList, DeviceResourceByUUID
from src.resources.resource_user import UserResourceList, UserResourceByUUID, UserResourceByUsername, \
    UserLoginResource, UserChangePasswordResource, UserVerifyResource, UserAuthenticateResource
from src.system.resources.ping import Ping

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
bp_users = Blueprint('users', __name__, url_prefix='/api/users')
bp_current_user = Blueprint('current_user', __name__, url_prefix='/api/current_user')
bp_devices = Blueprint('devices', __name__, url_prefix='/api/devices')

# 1
Api(bp_system).add_resource(Ping, '/ping')

# 2
api_users = Api(bp_users)
api_users.add_resource(UserResourceList, '')
api_users.add_resource(UserResourceByUUID, '/uuid/<string:uuid>')
api_users.add_resource(UserResourceByUsername, '/username/<string:username>')
api_users.add_resource(UserLoginResource, '/login')
api_users.add_resource(UserChangePasswordResource, '/change_password')
api_users.add_resource(UserVerifyResource, '/verify')
api_users.add_resource(UserAuthenticateResource, '/authenticate')

# 3
api_current_user = Api(bp_current_user)
api_current_user.add_resource(CurrentUserResource, '')

# 4
api_devices = Api(bp_devices)
api_devices.add_resource(DeviceResourceList, '')
api_devices.add_resource(DeviceResourceByUUID, '/uuid/<string:uuid>')
