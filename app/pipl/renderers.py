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
            response_dict = {
                'id': '',
                'coordinates': '',
                'name': ''
            }
            response_dict['id'] = data.get('features')[0]['id']
            response_dict['coordinates'] = data.get('features')[0]['geometry']['coordinates']
            response_dict['name'] = data.get('features')[0]['properties']['name']
            response = json.dumps({'data': response_dict})
        return response
