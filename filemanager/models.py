#coding: utf-8

from __future__ import absolute_import

import os
import base64
import mimetypes

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from .settings import ICONS_PATH_FORMAT_STR, AVAILABLE_ICONS, IMAGE_ICON_NAME, IMAGE_ICONS

def generate_file_path(instance, filename):
    filename_dict = {'filename': filename}
    filename = filename_dict['filename']
    
    return filename

class FileCategory(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    name = models.CharField(u"Nazwa", max_length=200)
    
    class Meta:
        verbose_name = u"Kategoria pliku"
        verbose_name_plural = u"Kategorie plików"
    
    def __unicode__(self):
        return self.name


class StaticFileQueryset(models.query.QuerySet):
    def images(self):
        return self.filter(
            reduce(lambda x, y: x | Q(filename__iendswith=y), StaticFile.IMAGE_EXTENSIONS, Q()))

class StaticFileManager(models.Manager):
    def get_query_set(self):
        return StaticFileQueryset(self.model, using=self._db)

    def images(self):
        return self.all().images()

class StaticFile(models.Model):
    IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png', 'bmp']

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    category = models.ForeignKey(FileCategory, verbose_name=u"Kategoria pliku", null=True)
    static_file = models.FileField(u"Plik", upload_to=generate_file_path)
    filename = models.CharField(u'Oryginalna nazwa pliku', max_length=100, blank=True,
                                help_text=u'Przy dodawaniu pliku nazwa zapisze się samoczynnie')
    description = models.CharField(u'Krótki opis', max_length=200,
                                   help_text=u'Wyświetlany w nazwie linka')
   
    objects = StaticFileManager()

    class Meta:
        verbose_name = u"Plik"
        verbose_name_plural = u"Pliki"
    
    def file_ext(self):
        try:
            return self.filename.split('.')[-1].lower()
        except IndexError:
            return ''
    file_ext.short_description = "Rozszerzenie pliku"
    
    def url(self):
        return self.static_file.storage.url(str(self.static_file))

    def as_base64(self):
        with open(self.file_path, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        return 'data:%s;base64,%s' % (mimetypes.guess_type(self.file_path)[0], encoded_string)

    def icon_path(self):
        ext = self.file_ext()
        if ext in AVAILABLE_ICONS:
            return ICONS_PATH_FORMAT_STR % ext
        elif ext in IMAGE_ICONS:
            return ICONS_PATH_FORMAT_STR % IMAGE_ICON_NAME
        else:
            return ''

    def size(self):
        if os.path.exists(self.file_path):
            return "%0.1f KB" % (os.path.getsize(self.file_path)/(1024.0))
        return "0 MB"

    @property
    def file_path(self):
        return '%s/%s' % (settings.MEDIA_ROOT, self.static_file.name.split("/")[-1])
    
    def __unicode__(self):
        return "%s - %s" % (unicode(self.static_file), self.filename)
