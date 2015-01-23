# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Polyconseil SAS. All rights reserved.f

from __future__ import unicode_literals
import base64
import os
import shutil
import tempfile
import zipfile

from pyramid.httpexceptions import HTTPMovedPermanently, HTTPMethodNotAllowed, HTTPForbidden, HTTPBadRequest
from pyramid.renderers import get_renderer

import wtforms
from wtforms import validators as wtvalidators

from dokang import api
from dokang import utils


def get_hit_limit(settings):
    if 'dokang.hit_limit' not in settings:
        return None
    hit_limit = int(settings['dokang.hit_limit'])
    if hit_limit == 0:
        return None
    return hit_limit


def search(request):
    settings = request.registry.settings
    doc_sets = settings['dokang.doc_sets']
    hit_limit = get_hit_limit(settings)
    raw_query = request.GET.get('query')
    only_doc_set = request.GET.get('doc_set')
    if raw_query:
        query = raw_query
        if only_doc_set:
            query += ' set:%s' % only_doc_set
        index_path = settings['dokang.index_path']
        hits = list(api.search(index_path, query, limit=hit_limit))
        for hit in hits:
            hit['doc_set_title'] = doc_sets[hit['set']]['title']
    else:
        hits = None
    return {
        'api': TemplateApi(request),
        'query': raw_query,
        'only_doc_set': only_doc_set,
        'doc_sets': sorted(doc_sets.values(), key=lambda d: d['title'].lower()),
        'hits': hits
    }


class TemplateApi(object):
    """
    Provide a master template and various information and utilities that can be used in any template.

    Not that we really need that for a single template but, well, that's what I usually do...
    """

    def __init__(self, request):
        self.request = request
        self.layout = get_renderer('templates/layout.pt').implementation()

    def route_url(self, route_name, *elements, **kw):
        return self.request.route_url(route_name, *elements, **kw)

    def hit_url(self, hit):
        doc_sets = self.request.registry.settings['dokang.doc_sets']
        base_url = self.request.static_url(doc_sets[hit['set']]['path'])
        return '/'.join((base_url, hit['path']))

    def static_url(self, path, **kw):
        if ':' not in path:
            path = 'dokang:%s' % path
        return self.request.static_url(path, **kw)


class DocUploadForm(wtforms.Form):
    name = wtforms.StringField('Package Name', validators=[wtvalidators.DataRequired('No package name given')])
    content = wtforms.FileField('Documentation Zip')

    @staticmethod
    def validate_content(form, field):
        if field.data.bufsize > 100 * 1024 * 1024:
            raise wtvalidators.ValidationError('ZIP file is too large')

        data_file = field.data.file
        if not zipfile.is_zipfile(data_file):
            raise wtvalidators.ValidationError('ZIP file is not a zipfile')

        zip_file = zipfile.ZipFile(data_file)
        members = zip_file.namelist()
        if 'index.html' not in members:
            raise wtvalidators.ValidationError('Top-level "index.html" missing in the ZIP file')

        base_dir = tempfile.mkdtemp()
        try:
            for name in members:
                if not os.path.normpath(os.path.join(base_dir, name)).startswith(base_dir):
                    raise wtvalidators.ValidationError('Invalid path name %s in the ZIP file', name)
        finally:
            os.rmdir(base_dir)

        data_file.seek(0)


def doc_upload(request):  # Route is not activated when dokang.uploaded_docs.dir is not set
    settings = request.registry.settings
    doc_dir = settings['dokang.uploaded_docs.dir']
    token = settings.get('dokang.uploaded_docs.token')

    bad_auth = (
        token is None or
        request.authorization is None or
        request.authorization[0] != 'Basic' or
        base64.b64decode(request.authorization[1]) != 'dokang:{0}'.format(token)
    )
    if bad_auth:
        raise HTTPForbidden()

    if not request.POST:
        raise HTTPMethodNotAllowed()

    if request.POST.get(':action', '--no-action--') != 'doc_upload':
        raise HTTPBadRequest('Only doc_upload action is supported.')

    form = DocUploadForm(request.POST)
    if not form.validate():
        raise HTTPBadRequest(form.errors)

    project = form.data['name']
    project_dir = os.path.join(doc_dir, project)

    zip_file = zipfile.ZipFile(form.data['content'].file)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    zip_file.extractall(project_dir)

    # update doc sets
    doc_set_info = settings['dokang.doc_sets'][project] = utils.doc_set(settings, project)

    # index new doc set
    index_path = settings['dokang.index_path']
    api.index_document_set(index_path, doc_set_info, False)

    return HTTPMovedPermanently(request.static_url(project_dir))
