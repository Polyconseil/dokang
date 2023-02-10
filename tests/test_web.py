# Copyright (c) Polyconseil SAS. All rights reserved.
import os
import shutil

from pyramid import testing

from dokang import api
from dokang import views
from dokang.harvesters import html_config


def get_data_path(*components):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'data',
        *components)


INDEX_PATH = get_data_path('whoosh_test_index')
UPLOAD_PATH = get_data_path('upload')


class TestWebFrontEnd:

    @classmethod
    def setup_class(cls):
        cls._prepare_index()

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(INDEX_PATH)

    def setup_method(self, method):
        self.config = testing.setUp()
        self.config.include('pyramid_chameleon')
        self.config.registry.settings['dokang.uploaded_docs.harvester'] = 'dokang.harvesters.html_config'
        self.config.registry.settings['dokang.uploaded_docs.dir'] = UPLOAD_PATH
        self.config.registry.settings['dokang.index_path'] = INDEX_PATH

    def teardown_method(self):
        testing.tearDown()

    @classmethod
    def _prepare_index(cls):
        api.initialize_index(INDEX_PATH)
        doc_set_info = {
            'id': 'test',
            'title': 'Test documentation',
            'path': get_data_path('upload', 'test'),
            'harvester': html_config()
        }
        api.index_document_set(INDEX_PATH, doc_set_info)

    def test_search(self):
        request = testing.DummyRequest()
        context = views.search(request)
        assert context['hits'] is None

        request = testing.DummyRequest(params={
            'query': 'ShouldBeIndexed',
            'doc_set': 'not-the-right-docset'})
        context = views.search(request)
        assert context['hits'] == []

        request = testing.DummyRequest(params={
            'query': 'ShouldBeIndexed'})
        context = views.search(request)
        hits = context['hits']
        assert len(hits) == 1
        assert hits[0]['doc_set_title'] == "Title of the test doc set"

    def test_opensearch(self):
        self.config.registry.settings['dokang.opensearch.name'] = 'Testing docs'
        self.config.registry.settings['dokang.opensearch.description'] = 'Testing docs'
        # The "opensearch" view returns links to the (static) favicon...
        self.config.add_static_view('static', 'dokang:static')
        # ... and a "search" route.
        self.config.add_route('search', '/')

        request = testing.DummyRequest()
        response = views.opensearch(request)
        assert response.content_type == 'application/opensearchdescription+xml'
