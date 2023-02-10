# Copyright (c) Polyconseil SAS. All rights reserved.
import os

from dokang import harvesters


def get_data_path(*components):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'data',
        *components)


class TestHtmlHarvester:

    def test_basics(self):
        path = get_data_path('harvesters', 'html.html')
        harvester = harvesters.HtmlHarvester()
        document = harvester.harvest_file(path)
        assert document['title'] == "The title"
        assert "ShouldBeIndexed" in document['content']
        assert "ShouldNotBeIndexed" not in document['content']

    def test_non_ascii_file(self):
        for filename in ('html.utf8.html', 'html.latin1.html'):
            path = get_data_path('harvesters', filename)
            harvester = harvesters.HtmlHarvester()
            document = harvester.harvest_file(path)
            assert document['title'] == "Un titre accentué"
            assert "accentué" in document['content']


class TestSphinxHarvester:

    def test_basics(self):
        path = get_data_path('harvesters', 'sphinx.html')
        harvester = harvesters.SphinxHarvester()
        document = harvester.harvest_file(path)
        assert document['title'] == "The title"
        assert "ShouldBeIndexed" in document['content']
        assert "ShouldNotBeIndexed" not in document['content']

    def test_non_ascii_file(self):
        path = get_data_path('harvesters', 'sphinx.latin1.html')
        harvester = harvesters.SphinxHarvester()
        document = harvester.harvest_file(path)
        assert document['title'] == "Un titre accentué"
        assert "accentué" in document['content']


class TestReadTheDocsSphinxHarvester:

    def test_basics(self):
        path = get_data_path('harvesters', 'sphinx_rtd.html')
        harvester = harvesters.ReadTheDocsSphinxHarvester()
        document = harvester.harvest_file(path)
        assert document['title'] == "The title"
        assert "ShouldBeIndexed" in document['content']
        assert "ShouldNotBeIndexed" not in document['content']


class TestComputeHash:
    def test_basics(self):
        for filename, known_hash in (
            ('html.utf8.html', '9bac2a167ae679a89d5f9f7df331f673'),
            ('html.latin1.html', '9d13dea55e12716bcf01a3f63868babb')):
            path = get_data_path('harvesters', filename)
            assert harvesters._compute_hash(path) == known_hash
