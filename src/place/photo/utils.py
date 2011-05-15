'''
Created on 2011-5-16

@author: James
'''
from django.http import HttpResponse
import json

def __get_json_response(cls, obj):
    return HttpResponse(__to_json(cls, obj), content_type='application/json')

def __to_json(cls, obj):
    return json.dumps(obj, default=cls.json_default)

def _add_thumb(s):
    parts = s.split('.')
    parts.insert(-1, 'thumb')
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return '.'.join(parts)
