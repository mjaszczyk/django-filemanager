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

class ImageWidget(Widget):
    class Media:
        js = (settings.STATIC_URL + 'media/js/media_fields.js', )
            
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
            'STATIC_URL': settings.STATIC_URL
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

# zasady zdefiniowane dla southa
rules = [
  (
    (ImageField,),
    [],
    {
        "to": ["rel.to", {}],
        "to_field": ["rel.field_name", {"default_attr": "rel.to._meta.pk.name"}],
        "related_name": ["rel.related_name", {"default": None}],
        "db_index": ["db_index", {"default": True}],
    },
  )
]
add_introspection_rules(rules, ["^apps\.filemanager\.fields\.ImageField"])
