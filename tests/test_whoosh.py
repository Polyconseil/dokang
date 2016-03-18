# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

import os
import shutil
try:  # Python 2.6 compatibility
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from dokang import api
from dokang.harvesters import html_config


def get_data_path(*components):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'data',
        *components)


class TestApi(TestCase):

    def tearDown(self):
        super(TestApi, self).tearDown()
        if os.path.exists(self.index_path):
            shutil.rmtree(self.index_path)

    @property
    def index_path(self):
        return get_data_path('whoosh_test_index')

    def test_integration(self):
        api.initialize_index(self.index_path)

        doc_set_info = {
            'id': 'test',
            'title': 'Test documentation',
            'path': get_data_path('upload', 'test'),
            'harvester': html_config()
        }
        api.index_document_set(self.index_path, doc_set_info)

        self.assertEqual(list(api.search(self.index_path, "ShouldNotBeIndexed")), [])
        hits = list(api.search(self.index_path, "ShouldBeIndexed"))
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]['path'], 'test1.html')
        self.assertEqual(hits[0]['title'], 'The title')
        self.assertEqual(hits[0]['set'], 'test')
        self.assertEqual(hits[0]['kind'], 'HTML')
        hits = list(api.search(self.index_path, "ShouldBeIndexed set:test"))
        self.assertEqual(len(hits), 1)
        self.assertEqual(list(api.search(self.index_path, "ShouldBeIndexed set:unknown")), [])

        api.clear_document_set(self.index_path, 'unknown')
        hits = list(api.search(self.index_path, "ShouldBeIndexed"))
        self.assertEqual(len(hits), 1)

        api.clear_document_set(self.index_path, doc_set_info['id'])
        self.assertEqual(list(api.search(self.index_path, "ShouldBeIndexed")), [])
