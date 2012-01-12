#coding: utf-8

from django.conf import settings

AVAILABLE_ICONS = ['zip', 'doc', 'xls', 'pdf']
IMAGE_ICONS = ['jpeg', 'png', 'gif', 'jpg']
IMAGE_ICON_NAME = 'img'
ICONS_PATH = settings.STATIC_URL + 'filemanager/icons/'
ICONS_PATH_FORMAT_STR = ICONS_PATH + '%s-icon.png'
