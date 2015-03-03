# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Polyconseil SAS. All rights reserved.f

from pyramid.config import Configurator
from pyramid.static import static_view

from dokang.utils import load_doc_sets


def make_app(global_settings, **settings):
    """Set up and return the WSGI application."""
    settings = load_doc_sets(settings)
    config = Configurator(settings=settings)

    # Third-party includes
    config.include('pyramid_chameleon')

    # Routes and views for static and home page
    config.add_static_view('static', 'static')
    config.add_route('search', '/')
    config.add_view('.views.search', route_name='search', renderer='templates/search.pt')

    # Upload endpoint
    config.add_route('doc_upload', '/upload')
    config.add_view('.views.doc_upload', route_name='doc_upload')

    # A catch-all route that serves documentation from the root of
    # Dokang.
    uploaded_docs_dir = settings.get('dokang.uploaded_docs.dir')
    static_doc_view = static_view(uploaded_docs_dir, use_subpath=True)
    config.add_route('catch_all_doc_view', '/*subpath')
    config.add_view(static_doc_view, route_name='catch_all_doc_view')

    return config.make_wsgi_app()
