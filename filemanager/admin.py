#coding: utf-8

from __future__ import absolute_import

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.conf.urls.defaults import patterns, url
from django.conf import settings

from .models import StaticFile, FileCategory
from seautils.baseadmin.admin import BaseModelAdmin
from seautils.utils import compile_js

class FileAdmin(BaseModelAdmin):
    class Media:
        js = compile_js(['filemanager/js/admin_list.coffee'])

    date_hierarchy = ('create_time')
    list_display = ('icon', 'static_file', 'category', 'create_time', 'file_ext')
    list_display_links = ('static_file', 'create_time', )
    list_filter = ('category',)
    search_fields = ('filename', 'description')
    
    exclude = ('author',)
     
    def icon(self, obj):
        return '<img width="100" src="%s" />' % obj.icon_path()
    icon.short_description = u'Ikona'
    icon.allow_tags = True

    def select_button(self, obj):
        return """<button ref="%d" name="%s" addr="%s" class="insert-button">Wstaw </button>""" \
                    % (obj.id, obj.filename, obj.static_file.url)
    select_button.allow_tags = True

    def save_form(self, request, form, change):
        obj = super( FileAdmin, self).save_form(request, form, change)
        if 'static_file' in request.FILES:
            obj.filename = request.FILES['static_file'].name
        
        if not change:
            obj.author = request.user
        return obj
        obj.save()

    def get_urls(self):
        urls = super(FileAdmin, self).get_urls()
        urls = patterns('',
            (r'^popuplist/(?P<media_type>\w+)/$', self.popup_list_view),
        ) + urls
        return urls

    def popup_list_view(self, request, media_type, extra_context=None):
        if not self.has_change_permission(request):
            raise PermissionDenied
        
        def queryset_modifier(queryset):
            if media_type == 'image':
                queryset = queryset.images()
            return queryset
        
        list_display = ['select_button'] + list(self.list_display)
        return self.simple_list_view(request, extra_context, list_display=list_display, 
                                     template_path=self.change_list_template, 
                                     queryset_modifier=queryset_modifier)
    
class FileCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(StaticFile, FileAdmin)
admin.site.register(FileCategory, FileCategoryAdmin)
