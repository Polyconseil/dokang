# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals
import base64
import itertools
import json
import os
import shutil
import tempfile
import zipfile

from pyramid.httpexceptions import HTTPMovedPermanently, HTTPMethodNotAllowed, HTTPForbidden, HTTPBadRequest
from pyramid.renderers import get_renderer
from pyramid.response import Response

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
    doc_sets = utils.get_doc_sets(settings)
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

    sorted_doc_sets = sorted(doc_sets.values(), key=lambda d: d['title'].lower())
    return {
        'api': TemplateApi(request),
        'query': raw_query,
        'only_doc_set': only_doc_set,
        'doc_sets': [
            (k.upper(), list(v))
            for k, v in itertools.groupby(sorted_doc_sets, key=lambda d: d['title'][0].lower())
        ],
        'hits': hits
    }


def opensearch(request):
    """Return OpenSearch description file."""
    settings = request.registry.settings
    params = {
        'name': settings['dokang.opensearch.name'],
        'description': settings['dokang.opensearch.description'],
        'favicon': request.static_url('dokang:static/img/favicon.ico'),
        'search_url': request.route_url('search'),
    }
    return Response(
        body="""<?xml version="1.0" encoding="UTF-8" ?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>%(name)s</ShortName>
  <Description>%(description)s</Description>
  <Image>%(favicon)s</Image>
  <InputEncoding>UTF-8</InputEncoding>
  <OutputEncoding>UTF-8</OutputEncoding>
  <Url type="text/html" template="%(search_url)s?query={searchTerms}"/>a
</OpenSearchDescription>""" % params,
        content_type=b'application/opensearchdescription+xml'
    )


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
        return self.doc_url(hit['set'], hit['path'])

    def doc_url(self, doc_set_id, path=''):
        # We suppose that the id of the document set is used to create
        # the upload directory. This is what `utils.doc_set()` does.
        # This assumption simplifies the code here.
        subpath = os.path.join(doc_set_id, path)
        return self.route_url('catch_all_doc_view', subpath=subpath)

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
        base64.b64decode(request.authorization[1]).decode('utf-8') != 'dokang:{0}'.format(token)
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
    metadata = utils.doc_set(settings, project)

    zip_file = zipfile.ZipFile(form.data['content'].file)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    zip_file.extractall(project_dir)

    with open(os.path.join(project_dir, '.dokang'), 'w') as fp:
        json.dump({'title': metadata['title']}, fp)

    # index new doc set
    index_path = settings['dokang.index_path']
    api.index_document_set(index_path, utils.doc_set(settings, project), force=False)

    return HTTPMovedPermanently(request.route_url('catch_all_doc_view', subpath=project))
