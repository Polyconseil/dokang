Advanced configuration and usage
================================

.. _advanced_harvester_config:

Configuring harvesters
----------------------

In the configuration file described in the :ref:`basics_configuration`
section of the previous chapter, you must tell Dokang how to analyze
files of your document set. For that you need to provide a harvester
configuration as a dictionary with the following keys:

exclude
    An optional list of regular expressions. If the relative path of a
    file matches one of these expressions, it will not be processed,
    unless it matches one of the expressions listed in ``include``.

include
    An optional list of regular expressions. If the relative path of a
    file matches one of these expressions, it will be processed even
    if the path also matches one of the ``exclude`` expressions.

    This makes easier to write exclude and include regular expressions.

The configuration must also indicate which harvester to use for each
supported file extension. The extensions must include the dot. Here is
an example of such a configuration:

.. code:: python

   {'.html': SphinxHarvester,
    'include': ('_download', ),
    'exclude': ('^genindex.html$', '^search.html$', '/?_.*')
   }

To make the configuration a bit easier, Dokang provides a few
utilities that build sane configurations for you. For example, the
code above is more or less equivalent to the following expression:

.. code:: python

   from dokang.harvesters import sphinx_html_config

   sphinx_html_config()

You may customize those pre-defined configurations, like this:

.. code:: python

   sphinx_html_config(
       include=your_own_list_of_reg_exps,
       exclude=your_own_list_of_reg_exps,
       pdf=PdfHarvester)

For a list of all harvesting configurations and harvesters, see the
:doc:`api` chapter.


.. _advanced_cli_ref:

Command line reference
----------------------

Herebelow are the list of available commands of the ``dokang`` command
line program:

``help``
    Display a list of commands and general options. Use ``dokang
    <command> --help`` to get help and a list of options for a
    specific command.

``init [--force]``
    Initialize the index. If the index already exists, Dokang will
    refuse to overwrite it unless you provide the ``--force`` option.

``index [--docset DOC_SET_ID]``
    Index all configured document sets or only the given document
    set. If a document has already been indexed, the index is updated.

``clear DOC_SET_ID``
    Remove the given document set from the index.

``search QUERY``
    Search the index.
