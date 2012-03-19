#coding: utf-8

from django import template

register = template.Library()

@register.simple_tag
def image(static_file, size, crop=None):
    return static_file.image_path(size, crop) if static_file else ''