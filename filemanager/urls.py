#coding: utf-8

from django.conf.urls import patterns, url

file_base = r'^img/(?P<file_id>\d+)'
urlpatterns = patterns('filemanager.views',
    url('^upload/(?P<signal_key>[a-z0-9_]+)/$', 'upload_file', name='filemanager.upload'),
    url('%s.jpg$' % file_base, 'serve_img', {'params': ''}, name='filemanager.serve_img'),
    url('%s,(?P<params>[0-9 a-z\,]*).jpg$' % file_base, 'serve_img', name='filemanager.serve_img')
)
