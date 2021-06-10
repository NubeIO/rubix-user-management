from src.resources.utils import map_rest_schema

user_site_all_attributes = {
    'user_uuid': {
        'type': str,
        'required': True,
    },
    'site_uuid': {
        'type': str,
        'required': True,
    }
}

user_site_return_attributes = {
    'uuid': {
        'type': str,
    },
    'user_uuid': {
        'type': str,
    },
    'site_uuid': {
        'type': str,
    },
}

user_site_nested_return_attributes = {
    'uuid': {
        'type': str,
    },
    'site_uuid': {
        'type': str,
    },
}

user_site_return_fields = {}
map_rest_schema(user_site_return_attributes, user_site_return_fields)

user_site_nested_return_fields = {}
map_rest_schema(user_site_nested_return_attributes, user_site_nested_return_fields)

user_site_all_fields = {}
map_rest_schema(user_site_all_attributes, user_site_all_fields)
map_rest_schema(user_site_return_attributes, user_site_all_fields)
