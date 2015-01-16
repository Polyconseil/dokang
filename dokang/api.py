# -*- coding: utf-8 -*-
# Copyright (c) 2014-2015 Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

import logging
import os

from dokang.backends import whoosh
from dokang import harvesters


logger = logging.getLogger(__name__)


# This API is very dependent on the Whoosh backend. This is not
# entirely unrelated to the fact that Whoosh is the only backend.
# There is a plan for this API, though. The plan is not to have a plan
# until we need one.


def initialize_index(index_path):
    """Initialize the index."""
    indexer = whoosh.WhooshIndexer(index_path)
    indexer.initialize()


def index_document_set(index_path, info, force=False):
    """Index or reindex the document set.

    ``info`` should be a single item of the ``DOC_SETS`` configuration
    dictionary.

    If ``force`` is provided, all documents are reindexed, ignoring
    their last modification time.
    """
    indexer = whoosh.WhooshIndexer(index_path)
    searcher = whoosh.WhooshSearcher(index_path)
    mtimes = searcher.get_modification_times()

    doc_set = info['id']
    logger.info('Indexing doc set "%s"...', doc_set)

    # Unindex documents that have been deleted from the document set.
    to_be_deleted = []
    for relative_path in mtimes[doc_set].keys():
        path = os.path.join(info['path'], relative_path)
        if not os.path.exists(path):
            logger.debug('Marking indexed document "%s" for deletion.', relative_path)
            to_be_deleted.append(relative_path)
    if to_be_deleted:
        indexer.delete_documents(to_be_deleted)

    # Index or update all documents, or ignore them according to
    # their last modification time.
    documents = harvesters.harvest_set(
        info['path'],
        doc_set,
        info['harvester'],
        mtimes.get(doc_set, {}),
        force)
    indexer.index_documents(documents)


def clear_document_set(index_path, doc_set):
    """Remove the whole document set from the index."""
    indexer = whoosh.WhooshIndexer(index_path)
    logger.info('Clearing document set "%s"', doc_set)
    indexer.clear_set(doc_set)


def search(index_path, query, limit=None):
    """Return hits matching the query, as an iterator."""
    searcher = whoosh.WhooshSearcher(index_path)
    return searcher.search(query, limit=limit)
