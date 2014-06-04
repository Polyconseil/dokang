# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.
from __future__ import unicode_literals

import argparse
import logging
import os
import sys

from dokang.backends import whoosh
from dokang import harvester
from dokang.utils import load_doc_sets
from dokang.version import VERSION
from dokang.compat import ConfigParser

logger = logging.getLogger("dokang")


def main():
    kwargs = vars(parse_args(sys.argv[1:]))
    callback = kwargs.pop('callback')
    settings = kwargs.pop('settings') or os.environ.get('DOKANG_SETTINGS')
    if not settings:
        sys.exit("You must provide the settings location.")
    kwargs['settings'] = load_settings(settings)
    return callback(**kwargs)


def init(settings, force):
    index_path = settings['dokang.index_path']
    indexer = whoosh.WhooshIndexer(index_path)
    if os.path.exists(index_path) and not force:
        sys.exit("Index already exists at %s. Use `--force` to overwrite it." % index_path)
    indexer.initialize()


def index(settings, only_doc_set=None):
    index_path = settings['dokang.index_path']
    indexer = whoosh.WhooshIndexer(index_path)
    for doc_set, info in settings['dokang.doc_sets'].items():
        if only_doc_set is not None and only_doc_set != doc_set:
            continue
        logger.info("Indexing doc set %s...", doc_set)
        documents = harvester.harvest_set(info['path'], doc_set)
        # FIXME: how can we detect if documents have been deleted?
        indexer.index_documents(documents)

def search(settings, query):
    index_path = settings['dokang.index_path']
    searcher = whoosh.WhooshSearcher(index_path)
    hits = list(searcher.search(query, limit=None))
    print "Found %d results." % len(hits)
    for hit in hits:
        print("[{set}] {title}".format(**hit).encode(sys.stdout.encoding))


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog="Dokang",
        description='A lightweight search engine for HTML documents.')
    parser.add_argument('--version', action='version', version='%%(prog)s %s' % VERSION)
    parser.add_argument('--settings',
        action='store', help="Path of the setting file.", metavar='PATH')

    subparsers = parser.add_subparsers()

    # init
    parser_init = subparsers.add_parser('init', help='Initialize the index.')
    parser_init.set_defaults(callback=init)
    parser_init.add_argument(
        '--force',
        action='store_true',
        help="If set, delete the index if it already exists.")

    # index
    parser_index = subparsers.add_parser('index', help='Populate the index.')
    parser_index.set_defaults(callback=index)
    parser_index.add_argument(
        '--docset',
        action='store',
        dest='only_doc_set',
        metavar='DOC_SET_ID',
        help="If set, only index the given document set.")

    # search
    parser_search = subparsers.add_parser('search', help="Search in the index.")
    parser_search.set_defaults(callback=search)
    parser_search.add_argument('query', metavar='QUERY')

    return parser.parse_args(args)


def load_settings(path):
    here = os.path.abspath(os.path.dirname(path))
    config = ConfigParser(defaults={'here': here})
    config.read(path)
    settings = dict(config.items('app:main'))
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    settings = load_doc_sets(settings)
    return settings


if __name__ == '__main__':
    main()
