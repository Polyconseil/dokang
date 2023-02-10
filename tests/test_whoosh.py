# Copyright (c) Polyconseil SAS. All rights reserved.
import os
import shutil

from dokang import api
from dokang.harvesters import html_config


def get_data_path(*components):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'data',
        *components)


class TestApi:

    def teardown_method(self, method):
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

        assert list(api.search(self.index_path, "ShouldNotBeIndexed")) == []
        hits = list(api.search(self.index_path, "ShouldBeIndexed"))
        assert len(hits) == 1
        assert hits[0]['path'] == 'test1.html'
        assert hits[0]['title'] == 'The title'
        assert hits[0]['set'] == 'test'
        assert hits[0]['kind'] == 'HTML'
        hits = list(api.search(self.index_path, "ShouldBeIndexed set:test"))
        assert len(hits) == 1
        assert list(api.search(self.index_path, "ShouldBeIndexed set:unknown")) == []

        api.clear_document_set(self.index_path, 'unknown')
        hits = list(api.search(self.index_path, "ShouldBeIndexed"))
        assert len(hits) == 1

        api.clear_document_set(self.index_path, doc_set_info['id'])
        assert list(api.search(self.index_path, "ShouldBeIndexed")) == []
