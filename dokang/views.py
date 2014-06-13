# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.f

from __future__ import unicode_literals

from pyramid.renderers import get_renderer

from dokang.backends import whoosh


def search(request):
    doc_sets = request.registry.settings['dokang.doc_sets']
    raw_query = request.GET.get('query')
    only_doc_set = request.GET.get('doc_set')
    if raw_query:
        index_path = request.registry.settings['dokang.index_path']
        searcher = whoosh.WhooshSearcher(index_path)
        query = raw_query
        if only_doc_set:
            query += ' set:%s' % only_doc_set
        results = list(searcher.search(query, limit=20))
        for hit in results:
            hit['doc_set_title'] = doc_sets[hit['set']]['title']
    else:
        results = None
    return {'api': TemplateApi(request),
            'query': raw_query,
            'only_doc_set': only_doc_set,
            'doc_sets': sorted(doc_sets.values(), key=lambda d: d['title'].lower()),
            'results': results}


class TemplateApi(object):
    """Provide a master template and various information and utilities
    that can be used in any template.

    Not that we really need that for a single template but, well,
    that's what I usually do...
    """

    def __init__(self, request):
        self.request = request
        self.layout = get_renderer('templates/layout.pt').implementation()

    def route_url(self, route_name, *elements, **kw):
        return self.request.route_url(route_name, *elements, **kw)

    def hit_url(self, hit):
        doc_sets = self.request.registry.settings['dokang.doc_sets']
        base_url = doc_sets[hit['set']]['url']
        return '/'.join((base_url, hit['path']))

    def static_url(self, path, **kw):
        if ':' not in path:
            path = 'dokang:%s' % path
        return self.request.static_url(path, **kw)
