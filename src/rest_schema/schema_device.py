from src.resources.utils import map_rest_schema

device_all_attributes = {
    'device_id': {
        'type': str,
        'required': True,
    },
    'platform': {
        'type': str,
        'required': False,
    },
}

device_return_attributes = {
    'uuid': {
        'type': str,
    },
    'user_uuid': {
        'type': str,
    },
    'device_id': {
        'type': str,
    },
    'device_name': {
        'type': str,
    },
    'platform': {
        'type': str,
        'nested': True,
        'dict': 'platform.name'
    },
    'kiosk': {
        'type': bool
    }
}

device_nested_return_attributes = {
    'uuid': {
        'type': str,
    },
    'device_id': {
        'type': str,
    },
    'platform': {
        'type': str,
        'nested': True,
        'dict': 'platform.name'
    },
}

device_return_fields = {}
map_rest_schema(device_return_attributes, device_return_fields)

device_nested_return_fields = {}
map_rest_schema(device_nested_return_attributes, device_nested_return_fields)

device_all_fields = {}
map_rest_schema(device_all_attributes, device_all_fields)
map_rest_schema(device_return_attributes, device_all_fields)
