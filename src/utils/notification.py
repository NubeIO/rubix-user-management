import json

import requests

from src import AppSetting


def send_fcm_notification(key, data: dict):
    url = AppSetting.default_fcm_url
    headers = {'Content-type': 'application/json', 'Authorization': f'key={key}'}
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    return json.loads(resp.content)
