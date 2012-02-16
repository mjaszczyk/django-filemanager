#coding: utf-8

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def image(static_file, size, crop=None):
    params = str(size)
    if crop:
        params += ',%s' % crop
    return reverse('filemanager.serve_img', kwargs={'file_id': static_file.id,
        'params': params})

    
