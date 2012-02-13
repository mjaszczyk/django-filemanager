#coding: utf-8

from django.conf import settings

AVAILABLE_ICONS = ['zip', 'doc', 'xls', 'pdf']
IMAGE_ICONS = ['jpeg', 'png', 'gif', 'jpg']
IMAGE_ICON_NAME = 'img'
ICONS_PATH = settings.STATIC_URL + 'filemanager/icons/'
ICONS_PATH_FORMAT_STR = ICONS_PATH + '%s-icon.png'



from django.conf import settings


# When True ThumbnailNode.render can raise errors
THUMBNAIL_DEBUG = False

# Backend
THUMBNAIL_BACKEND = 'sorl.thumbnail.base.ThumbnailBackend'

# Path to Imagemagick or Graphicsmagick ``convert`` and ``identify``.
THUMBNAIL_CONVERT = 'convert'
THUMBNAIL_IDENTIFY = 'identify'

# Storage for the generated thumbnails
THUMBNAIL_STORAGE = settings.DEFAULT_FILE_STORAGE

# Image format, common formats are: JPEG, PNG
# Make sure the backend can handle the format you specify
THUMBNAIL_FORMAT = 'JPEG'

# Colorspace, backends are required to implement: RGB, GRAY
# Setting this to None will keep the original colorspace.
THUMBNAIL_COLORSPACE = 'RGB'

# Should we upscale images by default
THUMBNAIL_UPSCALE = True

# Quality, 0-100
THUMBNAIL_QUALITY = 95

# Save as progressive when saving as jpeg
THUMBNAIL_PROGRESSIVE = True

# Orientate the thumbnail with respect to source EXIF orientation tag
THUMBNAIL_ORIENTATION = True

AVAILABLE_SIZES = getattr(settings, 'IMG_AVAILABLE_SIZES', (
    (100, 100),
    (200, 200),
    (100, 200),
    (300, 300),
    (300, 100),
)
)
