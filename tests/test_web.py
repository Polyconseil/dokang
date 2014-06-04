# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

import os
import shutil
from unittest import TestCase

from pyramid import testing

from dokang.backends import whoosh as whoosh_backend
from dokang import harvester
from dokang import views


def get_data_path(*components):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'data',
        *components)


INDEX_PATH = get_data_path('whoosh_test_index')
TEST_DOC_SETS = {
    'test': {
        'title': "Title of the test doc set",
    }
}

def make_request(**params):
    request = testing.DummyRequest(params=params)
    request.registry.settings['dokang.doc_sets'] = TEST_DOC_SETS
    request.registry.settings['dokang.index_path'] = INDEX_PATH
    return request


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

    def tearDown(self):
        testing.tearDown()

    @classmethod
    def _prepare_index(cls):
        indexer = whoosh_backend.WhooshIndexer(INDEX_PATH)
        indexer.initialize()
        docs = harvester.harvest_set(get_data_path('sphinx_rtd'), 'test')
        indexer.index_documents(docs)

    def test_search(self):
        request = make_request()
        context = views.index(request)
        self.assertEqual(context['results'], None)

        request = make_request(
            query='ShouldBeIndexed',
            doc_set='not-the-right-docset')
        context = views.index(request)
        self.assertEqual(context['results'], [])

        request = make_request(query='ShouldBeIndexed')
        context = views.index(request)
        hits = context['results']
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]['doc_set_title'], "Title of the test doc set")
