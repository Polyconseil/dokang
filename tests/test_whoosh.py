# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

import os
import shutil
try:  # Python 2.6 compatibility
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from dokang.backends import whoosh as whoosh_backend


def get_data_path(*components):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'data',
        *components)


class TestWhooshBackend(TestCase):

    def tearDown(self):
        super(TestWhooshBackend, self).tearDown()
        shutil.rmtree(self.index_path)

    @property
    def index_path(self):
        return get_data_path('whoosh_test_index')

    def test_integration(self):
        indexer = whoosh_backend.WhooshIndexer(self.index_path)
        indexer.initialize()
        docs = [{
            'title': 'TitleOfFoo',
            'content': 'ContentOfFoo',
            'path': 'foo.html',
            'set': 'set1',
            'kind': 'HTML'}]
        indexer.index_documents(docs)

        searcher = whoosh_backend.WhooshSearcher(self.index_path)
        results = list(searcher.search('NotIndexed'))
        self.assertEqual(len(results), 0)

        results = list(searcher.search('ContentOfFoo'))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['path'], 'foo.html')
        self.assertEqual(results[0]['title'], 'TitleOfFoo')
        self.assertEqual(results[0]['set'], 'set1')

        # Change the content of foo, reindex and make sure that we
        # cannot find the old content.
        docs[0]['content'] = 'NewContentOfFoo'
        indexer.index_documents(docs)
        results = list(searcher.search('ContentOfFoo'))
        self.assertEqual(len(results), 0)
        results = list(searcher.search('NewContentOfFoo'))
        self.assertEqual(len(results), 1)
