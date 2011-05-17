import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'cms.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/var/python/django/place-upload'
if path not in sys.path:
    sys.path.append(path)