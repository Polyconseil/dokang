# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

import argparse
import logging
import logging.config
import os
import shutil
import sys

from dokang import __version__
from dokang import api
from dokang import compat
from dokang.utils import get_doc_sets

logger = logging.getLogger(__name__)


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
    if os.path.exists(index_path) and not force:
        sys.exit("Index already exists at %s. Use `--force` to overwrite it." % index_path)
    api.initialize_index(index_path)


def index(settings, only_doc_set, force):
    index_path = settings['dokang.index_path']
    doc_sets = get_doc_sets(settings)
    for doc_set, info in doc_sets.items():
        if only_doc_set is not None and only_doc_set != doc_set:
            continue
        api.index_document_set(index_path, info, force)


def clear(settings, docset, purge=False):
    index_path = settings['dokang.index_path']
    api.clear_document_set(index_path, docset)
    if purge:
        logger.info('Deleting files of document set "%s".', docset)
        shutil.rmtree(os.path.join(settings['dokang.uploaded_docs.dir'], docset))


def search(settings, query):
    if isinstance(query, bytes):
        query = query.decode(sys.stdin.encoding)
    index_path = settings['dokang.index_path']
    hits = list(api.search(index_path, query, limit=None))
    compat.print_to_stdout("Found %d results." % len(hits))
    for hit in hits:
        compat.print_to_stdout("[{set}] [{path}] {title}".format(**hit))


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog="Dokang",
        description='A lightweight search engine for HTML documents.'
    )
    parser.add_argument('--version', action='version', version='%%(prog)s %s' % __version__)
    parser.add_argument('--settings', action='store', help="Path of the setting file.", metavar='PATH')

    subparsers = parser.add_subparsers()

    # init
    parser_init = subparsers.add_parser('init', help='Initialize the index.')
    parser_init.set_defaults(callback=init)
    parser_init.add_argument(
        '--force',
        action='store_true',
        help="If set, delete the index if it already exists."
    )

    # index
    parser_index = subparsers.add_parser('index', help='Populate the index.')
    parser_index.set_defaults(callback=index)
    parser_index.add_argument(
        '--docset',
        action='store',
        dest='only_doc_set',
        metavar='DOC_SET_ID',
        help="If set, only index the given document set."
    )
    parser_index.add_argument(
        '--force',
        action='store_true',
        help="If set, reindex all documents even those that have not been modified since the last indexation."
    )

    # clear
    parser_clear = subparsers.add_parser('clear', help='Remove a document set.')
    parser_clear.set_defaults(callback=clear)
    parser_clear.add_argument('--purge', action='store_true', help='Delete files of document set.')
    parser_clear.add_argument(
        'docset',
        action='store',
        metavar='DOC_SET_ID',
        help="The id of the document set to remove."
    )

    # search
    parser_search = subparsers.add_parser('search', help="Search in the index.")
    parser_search.set_defaults(callback=search)
    parser_search.add_argument('query', metavar='QUERY')

    return parser.parse_args(args)


def load_settings(path):
    here = os.path.abspath(os.path.dirname(path))
    config = compat.ConfigParser(defaults={'here': here})
    config.read(path)
    settings = dict(config.items('app:main'))
    logging.config.fileConfig(path)
    return settings


if __name__ == '__main__':
    main()
