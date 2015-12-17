# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

import logging
import os

from bs4 import BeautifulSoup

from dokang.harvesters.base import Harvester


logger = logging.getLogger(__name__)


class SphinxHarvester(Harvester):
    """Harvest content from the HTML rendered version of a Sphinx-based
    set of documents.

    We look at the rendered HTML and not the source files to avoid
    wrongly indexing files included with the ``include`` directive.
    """

    def harvest_file(self, path):
        with open(path, 'rb') as fp:
            html = fp.read()
        soup = BeautifulSoup(html, 'html.parser')
        title, content = self._retrieve_title_and_content(soup)
        # Sphinx adds this character after each heading.
        title = title.replace("¶", "")
        content = content.replace("¶", "")
        title = title.strip()
        content = content.strip()
        return {
            'title': title,
            'content': content,
            'kind': 'HTML',
        }

    def _retrieve_title_and_content(self, soup):
        # A 'div class="body"' element is generated by the default
        # theme. I am not sure about other themes, though. See
        # ReadTheDocsSphinxHarvester for a custom harvester.
        content_block = soup.find(class_='body')
        # We prefer not to use the <title> element because Sphinx
        # appends the title of the project to the title of the page.
        title = content_block.find('h1').get_text()
        content = content_block.get_text()
        return title, content


class ReadTheDocsSphinxHarvester(SphinxHarvester):
    """Harvest content from the HTML rendered version of a Sphinx-based
    set of documents that uses the "Read The Docs" theme.

    The "Read The Docs" theme does not generate the ``<div>`` that we
    look for in the super class. We have to look for a different one.
    """

    def _retrieve_title_and_content(self, soup):
        content_block = soup.find(role='main')
        title = content_block.find('h1').get_text()
        content = content_block.get_text()
        return title, content


def sphinx_config(harvester=SphinxHarvester, include=None, exclude=None, **extensions):
    """
    Return a configuration that is suitable for a Sphinx-based documentation.

    If the documentation uses "Read The Docs" theme, you should rather use ``sphinx_rtd_config``.
    """
    # Exclude automatically generated HTML files such as 'search.html'
    if include is None:
        include = ('_download', )
    if exclude is None:
        exclude = (
            '^genindex.html$',
            '^objects.inv$',
            '^search.html$',
            '^searchindex.js$',
            '%s?_.*' % os.path.sep
        )
    config = {
        'include': include,
        'exclude': exclude,
        'html': harvester,
        'htm': harvester,
    }
    config.update(extensions)
    return config


def sphinx_rtd_config(harvester=ReadTheDocsSphinxHarvester, include=None, exclude=None, **extensions):
    """Return a configuration that is suitable for a Sphinx-based documentation that uses the ReadTheDocs theme."""
    return sphinx_config(harvester=harvester, include=include, exclude=exclude, **extensions)
