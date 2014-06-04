# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.
"""This module defines functions that harvest HTML text and retrieve
their text and title.
"""

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from bs4 import BeautifulSoup


def harvest_set(base_dir, doc_set):
    """Harvest content from a set of documents."""
    documents = []
    for dirpath, _dirnames, filenames in os.walk(base_dir):
        for filename in filenames:
            if not filename.endswith('.html'):
                continue
            if filename in ('genindex.html', 'search.html'):
                continue
            path = os.path.join(dirpath, filename)
            doc = harvest_file(path)
            doc['path'] = os.path.relpath(doc['path'], base_dir)
            doc['set'] = doc_set
            documents.append(doc)
    return documents


def harvest_file(path):
    """Harvest content from a file."""
    with open(path) as fp:
        html = fp.read()
    soup = BeautifulSoup(html)
    # This is specific to the "Read the Docs" Sphinx theme. It may not
    # exist in other themes.
    content_block = soup.find(role='main')
    # soup.title.string.strip() could be use in the general case, but
    # Sphinx adds the title of the book at the end of it
    title = content_block.find('h1').get_text()
    content = content_block.get_text()
    # Sphinx adds this character after each heading.
    title = title.replace("¶", "")
    content = content.replace("¶", "")
    title = title.strip()
    content = content.strip()
    path = path.decode(sys.getfilesystemencoding() or 'utf-8')
    return {
        'title': title,
        'content': content,
        'path': path}
