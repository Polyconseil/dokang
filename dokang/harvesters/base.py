# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.

import abc


class Harvester:
    """An abstract class for all harvesters."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def harvest_file(self, path):
        """Harvest contents from the given file.

        This method must be implemented by subclasses. It should
        return None if the document is not to be indexed, or a
        dictionary that has the following keys.

        title
            The title of the document.

        content
            The concatenated content of the document.

        kind
            The kind of document: HTML, PDF, etc.
        """
        return None
