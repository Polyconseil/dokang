# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

import os
import shutil
try:  # Python 2.6 compatibility
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from pyramid import testing

from dokang import api
from dokang.harvesters import html_config
from dokang import views


def get_data_path(*components):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'data',
        *components)


INDEX_PATH = get_data_path('whoosh_test_index')
TEST_DOC_SETS = (
    # Minimal configuration with just what we need to test the web
    # frontend.
    {'test': {
      'title': "Title of the test doc set"}
    }
)


class TestWebFrontEnd(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestWebFrontEnd, cls).setUpClass()
        cls._prepare_index()

    @classmethod
    def tearDownClass(cls):
        super(TestWebFrontEnd, cls).tearDownClass()
        shutil.rmtree(INDEX_PATH)

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.registry.settings['dokang.doc_sets'] = TEST_DOC_SETS
        self.config.registry.settings['dokang.index_path'] = INDEX_PATH

    def tearDown(self):
        testing.tearDown()

    @classmethod
    def _prepare_index(cls):
        api.initialize_index(INDEX_PATH)
        doc_set_info = {
            'id': 'test',
            'title': 'Test documentation',
            'path': get_data_path('api'),
            'url': 'http://docs.exemple.com/',
            'harvester': html_config()
        }
        api.index_document_set(INDEX_PATH, doc_set_info)

    def test_search(self):
        request = testing.DummyRequest()
        context = views.search(request)
        self.assertEqual(context['hits'], None)

        request = testing.DummyRequest(params={
            'query': 'ShouldBeIndexed',
            'doc_set': 'not-the-right-docset'})
        context = views.search(request)
        self.assertEqual(context['hits'], [])

        request = testing.DummyRequest(params={
            'query': 'ShouldBeIndexed'})
        context = views.search(request)
        hits = context['hits']
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]['doc_set_title'], "Title of the test doc set")
