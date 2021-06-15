import datetime
import re
from typing import List

import jwt
from Crypto.Cipher import AES
from flask import current_app, request
from flask_restful import fields, reqparse, abort
from rubix_http.exceptions.exception import UnauthorizedException
from werkzeug.security import generate_password_hash

from src import AppSetting


def get_field_type(attr_type):
    if attr_type == int:
        return fields.Integer()
    elif attr_type == str:
        return fields.String()
    elif attr_type == bool:
        return fields.Boolean()
    elif attr_type == float:
        return fields.Float()


def map_rest_schema(schema, resource_fields):
    """
    Adds schema dict marshaled data to resource_fields dict
    """
    for attr in schema:
        # hack fix... change to make fields primary thing and switch get_field_type to return opposite
        if not isinstance(schema[attr]['type'], fields.Raw):
            resource_fields[attr] = get_field_type(schema[attr]['type'])
        else:
            resource_fields[attr] = schema[attr]['type']
        if schema[attr].get('nested', False):
            resource_fields[attr].__init__(attribute=schema[attr]['dict'])


def encode_jwt_token(uuid: str, username: str):
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
        'sub': uuid,
        'username': username
    }
    encoded = jwt.encode(payload, app_setting.secret_key, algorithm='HS256')

    return {
        'access_token': encoded,
        'token_type': 'JWT'
    }


def get_access_token():
    if 'Authorization' not in request.headers:
        raise UnauthorizedException('Authorization header is missing')
    return str.replace(str(request.headers['Authorization']), 'Bearer ', '')


def decode_jwt_token(token):
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    try:
        return jwt.decode(token, app_setting.secret_key, algorithms="HS256")
    except Exception as e:
        raise UnauthorizedException(str(e))


def encrypt_password(password):
    if len(password) < 8 or not re.search(r'[\d]+', password) or not re.search('[A-Z]+', password):
        error = f'Password must have least 8 characters, one digit & one upper case'
        raise ValueError(error)
    return generate_password_hash(password, method='sha256')


def parse_user_update():
    parser = reqparse.RequestParser()
    parser.add_argument('first_name', type=str, required=False, store_missing=False)
    parser.add_argument('last_name', type=str, required=False, store_missing=False)
    parser.add_argument('email', type=str, required=False, store_missing=False)
    args = parser.parse_args()
    return args


def aes_encrypt(plaintext) -> bytes:
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    secret, key = app_setting.fcm_secret_key.split(':')
    cipher = AES.new(key.encode('UTF-8'), AES.MODE_CTR, counter=lambda: secret.encode('UTF-8'))
    return cipher.encrypt(plaintext)


def aes_decrypt(ciphertext) -> str:
    app_setting = current_app.config[AppSetting.FLASK_KEY]
    secret, key = app_setting.fcm_secret_key.split(':')
    cipher = AES.new(key.encode('UTF-8'), AES.MODE_CTR, counter=lambda: secret.encode('UTF-8'))
    return cipher.decrypt(ciphertext).decode('UTF-8')


def authorize():
    open_endpoints: List[str] = ['apps_ping.ping', 'apps_users.create', 'apps_users.login', 'apps_users.check_username',
                                 'apps_users.check_email']
    if request.path[:10] != '/api/apps/':
        abort(401, message=str('You are not authorized!'))
    elif request.endpoint not in open_endpoints:
        try:
            access_token = get_access_token()
            decode_jwt_token(access_token)
        except Exception as e:
            abort(401, message=str(e))
