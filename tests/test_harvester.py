# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

import os
try:  # Python 2.6 compatibility
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from dokang import harvester


def get_data_path(*components):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'data',
        *components)

class TestHarvester(TestCase):

    def test_readthedocs_sphinx_document(self):
        doc_set = 'docset'
        path = get_data_path('sphinx_rtd')
        documents = harvester.harvest_set(path, doc_set)
        self.assertEqual(len(documents), 1)
        document = documents[0]
        self.assertEqual(document['title'], "The title")
        self.assertEqual(document['path'], 'index.html')
        self.assertEqual(document['set'], doc_set)
        self.assertIn("ShouldBeIndexed", document['content'])
        self.assertNotIn("ShouldNotBeIndexed", document['content'])
