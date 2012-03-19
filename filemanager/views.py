#coding: utf-8
from __future__ import absolute_import

import mimetypes

from django.http import Http404
from django.conf import settings as global_settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.dispatch.dispatcher import Signal
from django.core.urlresolvers import reverse

from .models import FileCategory, StaticFile
from .forms import StaticFileForm
from .img import ThumbnailBackend
from .settings import AVAILABLE_SIZES

from . import settings
from seautils.views.decorators import expire_in

file_uploaded = Signal(providing_args=["signal_key", "static_file_instance"])

def upload_file(request, signal_key):
    if not request.method == 'POST':
        raise Http404
    files = {}
    files['static_file'] = request.FILES['file']
    form_data = {'author': request.user,
            'category': FileCategory.objects.get_or_create(
                name=global_settings.CAREGIVERS_FILE_CATEGORY_NAME)[0],
            'filename': files['static_file'].name,
            'description': ' ' }
    form = StaticFileForm(form_data, files)
    if form.is_valid():
        static_file = form.save(commit=False)
        [setattr(static_file, k, v) for k, v in form_data.items()]
        static_file.save()
        file_uploaded.send(None, static_file_instance=static_file, signal_key=signal_key)
        if request.is_ajax():
            response = HttpResponse('{"jsonrpc" : "2.0", "result" : null, "id" : "id"}',
                    mimetype='text/plain; charset=UTF-8')
            return response
        else:
            return HttpResponseRedirect(reverse('plupload_sample.upload.views.upload_file'))

@expire_in(seconds=settings.THUMBNAIL_EXPIRES)
def serve_img(request, file_id, params, ext):
    """
    Params:
    size_index
    crop
    """
    params_list = params.split(',')
    try:
        size_index = int(params_list[0] if params else -1)
    except ValueError:
        raise Http404('Invalid params')
    try:
        size = AVAILABLE_SIZES[size_index - 1]
    except IndexError:
        raise Http404('Invalid size.')
    
    crop = None
    if len(params_list) > 1:
        crop = params_list[1]

    static_file = get_object_or_404(StaticFile, id=file_id)

    # TODO oryginalny rozmiar
    tb = ThumbnailBackend()
    size_str = "%sx%s" % (size[0], size[1]) if size != -1 else ''
    thumb_args = [static_file.static_file, size_str]
    thumb_kwargs = {}
    if crop:
        thumb_kwargs['crop'] = crop
    ni = tb.get_thumbnail(*thumb_args, **thumb_kwargs)

    mimetype, encoding = mimetypes.guess_type(static_file.filename)
    mimetype = mimetype or 'application/octet-stream'

    image_format = 'JPEG'
    ext = ext.lower()
    if ext == 'png':
        image_format = 'PNG'
    
    response = HttpResponse()
    ni.save(response, image_format, quality=settings.THUMBNAIL_QUALITY)
    response['Content-Type'] = '%s; charset=utf-8' % (mimetype)
    return response
