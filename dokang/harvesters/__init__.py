# -*- coding: utf-8 -*-
# Copyright (c) 2011-2015 Polyconseil SAS. All rights reserved.

import logging
import os
import re

from .base import Harvester  # pylint: disable=unused-import
from .html import html_config, HtmlHarvester  # pylint: disable=unused-import
from .sphinx import (  # pylint: disable=unused-import
    sphinx_config, sphinx_rtd_config,
    SphinxHarvester, ReadTheDocsSphinxHarvester
)


logger = logging.getLogger(__name__)


def _must_process_path(path, include, exclude):
    for exp in include:
        if exp.match(path):
            return True
    for exp in exclude:
        if exp.match(path):
            return False
    return True


def harvest_set(base_dir, doc_set, config, mtimes, force):
    """Harvest a document set and return documents as dictionaries.

    ``config`` is the harvester configuration. It should contain a key
    for each supported file extensions. ``mtimes`` is a dictionary
    that links the path of each indexed file to its last modification
    time. ``force`` indicates whether to reindex a document even if it
    has not ben modified since the last indexation.

    This function is a generator. It yields dictionaries. Each
    dictionary should represent a document and contain the following
    keys in addition to the keys returned by the harvester itself.
    Each text-like value should be a string (in Python 3) or a unicode
    object (in Python 2).

    path
        The path of the document relative to the root of the document
        set.
    set
        The id of the document set. It should be ``doc_set``.
    """
    config_copy = config.copy()
    include = [re.compile(exp) for exp in config_copy.pop('include') or ()]
    exclude = [re.compile(exp) for exp in config_copy.pop('exclude') or ()]
    extensions = config_copy
    for dir_path, _dir_names, file_names in os.walk(base_dir):
        for filename in file_names:
            path = os.path.join(dir_path, filename)
            relative_path = os.path.relpath(path, base_dir)
            if not _must_process_path(relative_path, include, exclude):
                logger.debug('Excluded file "%s": include/exclude rules.', relative_path)
                continue
            _, extension = os.path.splitext(filename)
            extension = extension.lstrip('.')  # remove leading dot
            harvester_class = extensions.get(extension)
            if harvester_class is None:
                logger.debug('Excluded file "%s": no harvester found for %s.', relative_path, extension)
                continue
            modification_time = os.path.getmtime(path)
            indexed_modification_time = mtimes.get(relative_path)
            if not force and (indexed_modification_time and indexed_modification_time >= modification_time):
                logger.debug('Excluded file: "%s": not modified since last indexation.', relative_path)
                continue
            try:
                logger.debug('Indexing file "%s"', relative_path)
                doc = harvester_class().harvest_file(path)
            except Exception:  # pylint: disable=broad-except
                logger.exception("Could not index document %s", path)
            else:
                if doc:
                    doc['path'] = relative_path
                    doc['set'] = doc_set
                    doc['mtime'] = modification_time
                    yield doc
