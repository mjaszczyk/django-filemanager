#coding: utf-8

from __future__ import absolute_import

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.dispatch.dispatcher import Signal
from django.core.urlresolvers import reverse

from apps.filemanager.models import FileCategory
from .forms import StaticFileForm

file_uploaded = Signal(providing_args=["signal_key", "static_file_instance"])

def upload_file(request, signal_key):
    if not request.method == 'POST':
        raise Http404
    files = {}
    files['static_file'] = request.FILES['file']
    form_data = {'author': request.user,
            'category': FileCategory.objects.get_or_create(
                name=settings.CAREGIVERS_FILE_CATEGORY_NAME)[0],
            'filename': files['static_file'].name,
            'description': ' ' }
    form = StaticFileForm(form_data, files)
    if form.is_valid():
        static_file = form.save(commit=False)
        [setattr(static_file, k, v) for k, v in form_data.items()]
        static_file.save()
        file_uploaded.send(None, static_file_instance=static_file, signal_key=signal_key)
        if request.is_ajax():
            response = HttpResponse('{"jsonrpc" : "2.0", "result" : null, "id" : "id"}', mimetype='text/plain; charset=UTF-8')
            return response
        else:
            return HttpResponseRedirect(reverse('plupload_sample.upload.views.upload_file'))
