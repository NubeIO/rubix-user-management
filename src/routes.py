from flask import Blueprint
from flask_restful import Api

from src.resources.resource_device import DeviceResourceList, DeviceResourceByUUID
from src.resources.resource_user import UserResource, UserAuthenticateResource, UserLoginResource, \
    UserChangePasswordResource
from src.resources.resource_users import UsersResourceList, UsersResourceByUUID, UsersResourceByUsername, \
    UsersVerifyResource
from src.system.resources.ping import Ping

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
bp_users = Blueprint('users', __name__, url_prefix='/api/users')
bp_user = Blueprint('current_user', __name__, url_prefix='/api/user')

# 1
Api(bp_system).add_resource(Ping, '/ping')

# 2
api_users = Api(bp_users)
api_users.add_resource(UsersResourceList, '')
api_users.add_resource(UsersResourceByUUID, '/uuid/<string:uuid>')
api_users.add_resource(UsersResourceByUsername, '/username/<string:username>')
api_users.add_resource(UsersVerifyResource, '/verify')

# 3
api_user = Api(bp_user)
api_user.add_resource(UserResource, '')
api_user.add_resource(UserLoginResource, '/login')
api_user.add_resource(UserChangePasswordResource, '/change_password')
api_user.add_resource(UserAuthenticateResource, '/authenticate')
api_user.add_resource(DeviceResourceList, '/devices')
api_user.add_resource(DeviceResourceByUUID, '/devices/uuid/<string:uuid>')
