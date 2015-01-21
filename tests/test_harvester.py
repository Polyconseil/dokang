# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

import os
try:  # Python 2.6 compatibility
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from dokang import harvesters


def get_data_path(*components):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'data',
        *components)


class TestHtmlHarvester(TestCase):

    def test_basics(self):
        path = get_data_path('harvesters', 'html.html')
        harvester = harvesters.HtmlHarvester()
        document = harvester.harvest_file(path)
        self.assertEqual(document['title'], "The title")
        self.assertIn("ShouldBeIndexed", document['content'])
        self.assertNotIn("ShouldNotBeIndexed", document['content'])


class TestSphinxHarvester(TestCase):

    def test_basics(self):
        path = get_data_path('harvesters', 'sphinx.html')
        harvester = harvesters.SphinxHarvester()
        document = harvester.harvest_file(path)
        self.assertEqual(document['title'], "The title")
        self.assertIn("ShouldBeIndexed", document['content'])
        self.assertNotIn("ShouldNotBeIndexed", document['content'])


class TestReadTheDocsSphinxHarvester(TestCase):

    def test_basics(self):
        path = get_data_path('harvesters', 'sphinx_rtd.html')
        harvester = harvesters.ReadTheDocsSphinxHarvester()
        document = harvester.harvest_file(path)
        self.assertEqual(document['title'], "The title")
        self.assertIn("ShouldBeIndexed", document['content'])
        self.assertNotIn("ShouldNotBeIndexed", document['content'])
