'''
Created on 2011-4-12

@author: James
'''

from django.conf.urls.defaults import patterns, url
from cms.photo.views import upload, get

urlpatterns = patterns('',
    url(r'^upload/$', upload),
    url(r'^get/(?P<post_id>\w+)/$', get),
)
