from flask import Blueprint
from flask_restful import Api

from src.resources.resource_device import DeviceResourceList, DeviceResourceByUUID
from src.resources.resource_mqtt_topics import MqttTopicsResource
from src.resources.resource_user import UserResource
from src.resources.resource_users import *
from src.system.resources.ping import Ping

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
bp_users = Blueprint('users', __name__, url_prefix='/api/users')
bp_user = Blueprint('current_user', __name__, url_prefix='/api/user')
bp_mqtt_topics = Blueprint('mqtt_topics', __name__, url_prefix='/api/mqtt/topics')

# 1
Api(bp_system).add_resource(Ping, '/ping')

# 2
api_users = Api(bp_users)
api_users.add_resource(UsersResourceList, '')
api_users.add_resource(UsersLoginResource, '/login')
api_users.add_resource(UsersChangePasswordResource, '/change_password')
api_users.add_resource(UsersResourceByUUID, '/uuid/<string:uuid>')
api_users.add_resource(UsersResourceByUsername, '/username/<string:username>')
api_users.add_resource(UsersVerifyResource, '/verify')
api_users.add_resource(UsersCheckByUsernameResource, '/check/username')
api_users.add_resource(UsersCheckByEmailResource, '/check/email')
api_users.add_resource(UsersAuthenticateResource, '/authenticate')
api_users.add_resource(UsersRefreshToken, '/refresh_token')

# 3
api_user = Api(bp_user)
api_user.add_resource(UserResource, '')
api_user.add_resource(DeviceResourceList, '/devices')
api_user.add_resource(DeviceResourceByUUID, '/devices/uuid/<string:uuid>')

# 4
api_mqtt_topics = Api(bp_mqtt_topics)
api_mqtt_topics.add_resource(MqttTopicsResource, '')
