from rest_framework import renderers
import json
from rest_framework.response import Response


class TagRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'Error' in str(data):
            response = json.dumps({'errors': data})
        else:
            if data['type'] == 'Feature':
                response_dict = {
                    'id': '',
                    'coordinates': '',
                    'name': ''
                }
                response_dict['id'] = data.get('id')
                response_dict['coordinates'] = data.get('geometry')['coordinates']
                response_dict['name'] = data.get('properties')['name']
                response = json.dumps(response_dict)
            elif data['type'] == 'FeatureCollection':
                res_list = []
                for feature in data['features']:
                    response_dict = {
                        'id': '',
                        'coordinates': '',
                        'name': ''
                    }
                    response_dict['id'] = feature['id']
                    response_dict['coordinates'] = feature['geometry']['coordinates']
                    response_dict['name'] = feature['properties']['name']
                    res_list.append(response_dict)
                    response = json.dumps(res_list)
        return response
