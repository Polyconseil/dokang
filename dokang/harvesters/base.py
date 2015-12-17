# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.

import abc


class Harvester(object):
    """An abstract class for all harvesters."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def harvest_file(self, path):
        """Harvest contents from the given file.

        This method must be implemented by subclasses. It should
        return None if the document is not to be indexed, or a
        dictionary that has the following keys. Each text-like value
        should be a string (in Python 3) or a unicode object (in
        Python 2).

        title
            The title of the document.

        content
            The concatenated content of the document.

        kind
            The kind of document: HTML, PDF, etc.
        """
        return None
