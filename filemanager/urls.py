#coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('filemanager.views',
    url('^upload/(?P<signal_key>[a-z0-9_]+)/$', 'upload_file', name='filemanager.upload')        
)
