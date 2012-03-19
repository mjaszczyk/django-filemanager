#coding: utf-8
from __future__ import absolute_import

from django.conf.urls import patterns, url
from . import views

file_base = r'^img/(?P<file_id>\d+)'
urlpatterns = patterns('filemanager.views',
    url('^upload/(?P<signal_key>[a-z0-9_]+)/$', views.upload_file, name='filemanager.upload') ,
    url('%s.(?P<ext>[a-z0-9_]+)$' % file_base, 'serve_img', {'params': ''}, name='filemanager.serve_img'),
    url('%s,(?P<params>[0-9 a-z\,%%]*).(?P<ext>[a-z0-9_]+)$' % file_base, 'serve_img', name='filemanager.serve_img'),
)
