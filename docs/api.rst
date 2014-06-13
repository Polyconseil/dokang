API
===

Backends
--------

.. automodule:: dokang.backends.whoosh
   :members: WhooshIndexer, WhooshSearcher
   :member-order: bysource


Predefined harvesting configuration
-----------------------------------

.. autofunction:: dokang.harvesters.html.html_config

.. autofunction:: dokang.harvesters.sphinx.sphinx_config

.. autofunction:: dokang.harvesters.sphinx.sphinx_rtd_config


Harvesters
----------

.. autoclass:: dokang.harvesters.base.Harvester

.. autoclass:: dokang.harvesters.html.HtmlHarvester

.. autoclass:: dokang.harvesters.sphinx.SphinxHarvester

.. autoclass:: dokang.harvesters.sphinx.ReadTheDocsSphinxHarvester
