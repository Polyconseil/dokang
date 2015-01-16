# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Polyconseil SAS. All rights reserved.f
"""Index and search backends for Whoosh."""

from __future__ import absolute_import

from collections import defaultdict
import os
import shutil

from whoosh.fields import ID, Schema, STORED, TEXT
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
            path=ID(stored=True),
            set=ID(stored=True),
            mtime=STORED,  # not searchable
            title=TEXT(stored=True),
            content=TEXT(stored=False),
            kind=TEXT(stored=True),
        )
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
        needs_commit = False
        for document in documents:
            needs_commit = True
            writer.update_document(
                uid=':'.join((document['set'], document['path'])),
                path=document['path'],
                set=document['set'],
                mtime=document['mtime'],
                title=document['title'],
                content=document['content'],
                kind=document['kind'],
            )
        # optimize=True results in slower indexation but faster
        # search. That will do.
        if needs_commit:
            writer.commit(optimize=True)

    def delete_documents(self, paths):
        """Delete documents from the index."""
        index = open_dir(self.index_path)
        writer = index.writer()
        # FIXME: could we avoid the loop?
        for path in paths:
            writer.delete_by_term('path', path)
        writer.commit(optimize=True)


class WhooshSearcher(object):
    """Encapsulate search through Whoosh."""

    def __init__(self, index_path):
        self.index = open_dir(index_path)

    def get_modification_times(self):
        """Return the last modification time of each indexed document."""
        # It is not as heavy as it seems.
        mtimes = defaultdict(dict)
        with self.index.searcher() as searcher:
            for doc in searcher.all_stored_fields():
                mtimes[doc['set']][doc['path']] = doc['mtime']
        return mtimes

    def search(self, query_string, limit=None):
        """Search the query string in the index."""
        parser = MultifieldParser(('title', 'content'), self.index.schema)
        query = parser.parse(query_string)
        with self.index.searcher() as searcher:
            # FIXME: is there any point in yielding here? There will
            # not be a large number of hits anyway, so it would make
            # sense to return a simple list instead.
            for hit in searcher.search(query, limit=limit):
                yield {
                    'path': hit['path'],
                    'title': hit['title'],
                    'set': hit['set'],
                    'kind': hit['kind'],
                }
