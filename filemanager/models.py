#coding: utf-8

from __future__ import absolute_import

import os

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from PIL import Image

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

    create_time = models.DateTimeField(u'stworzony', auto_now_add=True)
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

    def icon_path(self):
        ext = self.file_ext()
        if ext in AVAILABLE_ICONS:
            return ICONS_PATH_FORMAT_STR % ext
        elif ext in IMAGE_ICONS:
            return self.url()
            return ICONS_PATH_FORMAT_STR % IMAGE_ICON_NAME
        else:
            return ''

    def size(self):
        file_path = '%s/%s' \
             % (settings.MEDIA_ROOT, self.static_file.name.split("/")[-1])
        if os.path.exists(file_path):
            return "%0.1f KB" % (os.path.getsize(file_path)/(1024.0))
        return "0 MB"
    
    def __unicode__(self):
        return "%s - %s" % (unicode(self.static_file), self.filename)

    def resized_content(self):
        _filter = getattr(Image, self.resize_args['filter'])
        size = (int(self.resize_args['new_w']), int(self.resize_args['new_h']))
        img = Image.open(self.image)
        new_image = img.resize(size, _filter)
        new_name = self.storage.get_available_name(self.args['file'])
        new_image.save(self.storage.path(new_name))
