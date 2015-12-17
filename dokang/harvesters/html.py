# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.

from __future__ import unicode_literals

from bs4 import BeautifulSoup

from dokang.harvesters.base import Harvester


class HtmlHarvester(Harvester):
    """Harvest content from HTML files."""

    def harvest_file(self, path):
        with open(path, 'rb') as fp:
            html = fp.read()
        soup = BeautifulSoup(html, 'html.parser')
        title, content = self._retrieve_title_and_content(soup)
        return {
            'title': title,
            'content': content,
            'kind': 'HTML',
        }

    @staticmethod
    def _retrieve_title_and_content(soup):
        title = soup.title.string.strip()
        content = soup.find('body').get_text().strip()
        return title, content


def html_config(harvester=HtmlHarvester, include=None, exclude=None, **extensions):
    """Return a configuration that is suitable for an HTML document set."""
    config = {
        'include': include,
        'exclude': exclude,
        'html': harvester,
        'htm': harvester,
    }
    config.update(extensions)
    return config
