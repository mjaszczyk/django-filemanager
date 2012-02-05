#coding: utf-8
from __future__ import absolute_import

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url('^upload/(?P<signal_key>[a-z0-9_]+)/$', views.upload_file, name='filemanager.upload') 
)
