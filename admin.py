#coding: utf-8

from __future__ import absolute_import

from django.contrib import admin

from .models import StaticFile, FileCategory

class FileAdmin(admin.ModelAdmin):
    date_hierarchy = ('create_time')
    list_display = ('static_file', 'category', 'create_time', 'file_ext')
    list_display_links = ('static_file', 'create_time', )
    list_filter = ('category',)
    search_fields = ('filename', 'description')
    
    exclude = ('author',)
     
    def save_form(self, request, form, change):
        obj = super( FileAdmin, self).save_form(request, form, change)
        if 'file' in request.FILES:
            obj.filename = request.FILES['file'].name
        
        if not change:
            obj.author = request.user
        return obj
    
class FileCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(StaticFile, FileAdmin)
admin.site.register(FileCategory, FileCategoryAdmin)
