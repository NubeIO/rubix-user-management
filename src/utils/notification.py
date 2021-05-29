import json

import requests

from src import AppSetting
from src.models.enum import FcmDataType


def send_fcm_notification(key, device_id):
    url = AppSetting.default_fcm_url
    headers = {'Content-type': 'application/json', 'Authorization': f'key={key}'}
    data = {
        "to": device_id,
        "notification": {
            "title": "NubeIO User Status",
            "body": "User is verified by Admin!"
        },
        "data": {
            "type": FcmDataType.USER_VERIFICATION.name
        }
    }
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    return json.loads(resp.content)
