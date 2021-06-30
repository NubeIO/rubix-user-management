from src.resources.utils import map_rest_schema

site_all_attributes = {
    'name': {
        'type': str,
        'required': True,
    },
    'address': {
        'type': str,
        'required': False,
    },
    'city': {
        'type': str,
        'required': False,
    },
    'state': {
        'type': str,
        'required': False,
    },
    'zip': {
        'type': int,
        'required': False,
    },
    'country': {
        'type': str,
        'required': False,
    },
    'lat': {
        'type': float,
        'required': False,
    },
    'lon': {
        'type': float,
        'required': False,
    },
    'time_zone': {
        'type': str,
        'required': False,
    },

}

site_return_attributes = {
    'uuid': {
        'type': str,
    }
}

site_return_fields = {}
map_rest_schema(site_return_attributes, site_return_fields)
map_rest_schema(site_all_attributes, site_return_fields)

site_all_fields = {}
map_rest_schema(site_all_attributes, site_all_fields)
map_rest_schema(site_return_attributes, site_all_fields)
