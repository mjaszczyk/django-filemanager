#coding: utf-8

from __future__ import absolute_import

from django.forms.models import ModelChoiceField
from django.db.models import ForeignKey
from django.forms.widgets import Widget
from django.template.loader import render_to_string
from django.forms.util import flatatt
from django.conf import settings

from south.modelsinspector import add_introspection_rules

from .models import StaticFile
from seautils.utils import compile_js

class ImageWidget(Widget):
    POPUP_ADDR_BASE = '/staticfile/popuplist/image/'
    POPUP_ADDR_PREFIX = '/filemanager'
    DEFAULT_POPUP_ADDR = '%s%s' % (POPUP_ADDR_PREFIX, POPUP_ADDR_BASE)

    class Media:
        js = compile_js(['filemanager/js/image_field.coffee', ])

    def __init__(self, *args, **kwargs):
        self.popup_addr = kwargs.pop('popup_addr', self.DEFAULT_POPUP_ADDR)
        print args, kwargs
        super(ImageWidget, self).__init__(*args, **kwargs)
            
    def render(self, name, value, attrs=None):
        if value == None:
            value = ''

        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs['type'] = 'hidden'

        # wyciagniecie odpowiedniego media dla podanego id
        try:
            media = StaticFile.objects.get(id=value)
        except StaticFile.DoesNotExist:
            media = None
        except ValueError:
            media = None

        return render_to_string('filemanager/_image_field.html', {
            'value': value,
            'final_attrs': final_attrs,
            'flat_attrs': flatatt(final_attrs),
            'media': media,
            'what': 'image',
            'STATIC_URL': settings.STATIC_URL,
            'popup_addr': self.popup_addr,
            'popup_addr_base': self.POPUP_ADDR_BASE
        })

class ImageFormField(ModelChoiceField):
    """
    Pole formowe uzywane dla pola ImageField
    """
    widget = ImageWidget

class ImageField(ForeignKey):
    """
    Pole w bazie bedace praktycznie ForeignKey (inny widget)
    """
    def __init__(self, *args, **kwargs):
        argsl = list(args)
        if 'to' in kwargs:
            kwargs['to'] = StaticFile
        else:
            if argsl:
                argsl[0] = StaticFile
            else:
                argsl.append(StaticFile)
        super(ImageField, self).__init__(*tuple(argsl), **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': ImageFormField,
        }
        defaults.update(kwargs)
        return super(ImageField, self).formfield(**defaults)

class ImageVideoField(ImageField):
    pass

# zasady zdefiniowane dla southa
rules = [
  (
    (ImageField, ImageVideoField),
    [],
    {
        "to": ["rel.to", {}],
        "to_field": ["rel.field_name", {"default_attr": "rel.to._meta.pk.name"}],
        "related_name": ["rel.related_name", {"default": None}],
        "db_index": ["db_index", {"default": True}],
    },
  )
]
add_introspection_rules(rules, ["^filemanager\.fields\.ImageField"])
