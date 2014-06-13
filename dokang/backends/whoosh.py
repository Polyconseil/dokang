# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.f
"""Index and search backends for Whoosh."""

from __future__ import absolute_import

import os
import shutil

from whoosh.fields import ID, Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser


class WhooshIndexer(object):
    """Encapsulate indexation through Whoosh."""

    def __init__(self, index_path):
        self.index_path = index_path

    def initialize(self):
        """Initialize the index.

        If an index already exists, it is deleted and recreated from
        scratch.
        """
        # FIXME: use NGRAM instead of TEXT?
        # FIXME: play with 'field_boost' parameter
        schema = Schema(
            uid=ID(stored=False, unique=True),
            title=TEXT(stored=True),
            content=TEXT(stored=False),
            path=ID(stored=True),
            set=ID(stored=True))
        if os.path.exists(self.index_path):
            shutil.rmtree(self.index_path)
        os.mkdir(self.index_path)
        create_in(self.index_path, schema)

    def clear_set(self, doc_set):
        """Remove all documents of this set from the index."""
        index = open_dir(self.index_path)
        index.delete_by_term('set', doc_set)

    def index_documents(self, documents):
        """Add or update documents in the index."""
        index = open_dir(self.index_path)
        writer = index.writer()
        for document in documents:
            # FIXME: store file last modification time, so that we can
            # update (or not update) an existing document.
            writer.update_document(
                uid=':'.join((document['set'], document['path'])),
                title=document['title'],
                content=document['content'],
                path=document['path'],
                set=document['set'])
        # optimize=True results in slower indexation but faster
        # search. That will do.
        writer.commit(optimize=True)


class WhooshSearcher(object):
    """Encapsulate search through Whoosh."""

    def __init__(self, index_path):
        self.index = open_dir(index_path)

    def search(self, query_string, limit=None):
        """Search the query string in the index."""
        parser = MultifieldParser(
            ('title', 'content'), self.index.schema)
        query = parser.parse(query_string)
        with self.index.searcher() as searcher:
            # FIME: is there any point in yielding here? There will
            # not be a large number of hits anyway, so it would make
            # sense to return a simple list instead.
            for hit in searcher.search(query, limit=limit):
                yield {
                    'path': hit['path'],
                    'title': hit['title'],
                    'set': hit['set']}
