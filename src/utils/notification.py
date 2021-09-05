import json

import requests

from src import AppSetting
from src.models.enum import Platform


def send_fcm_notification(key: str, data: dict, platform: Platform):
    url = AppSetting.default_fcm_url
    headers = {'Content-type': 'application/json', 'Authorization': f'key={key}'}
    data_clone = {**data}  # cloning because reference data shouldn't get updated over iteration
    if Platform.ANDROID == platform:
        del data_clone['notification']
    resp = requests.post(url, data=json.dumps(data_clone), headers=headers)
    return json.loads(resp.content)
