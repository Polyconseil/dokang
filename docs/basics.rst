Basics
======

In this chapter, we will skim over the installation and configuration
to search in the documentation of Dokang itself.


Concepts
--------

A key concept in Dokang is the "document set". A document set
represents a set of related documents (files) that resides in a
directory (and its sub-directories), for example the documentation of
a single project. You may instruct Dokang to index one or more
document sets, and then search in all or only a single set. It's so
new and brilliant that I am going to trademark and patent all this.


Installation
------------

In a brand new virtual environment, install with ``pip install
Dokang``, or ``pip install -r requirements.txt`` if you have cloned
the Git repository.


.. _basics_configuration:

Configuration
-------------

.. note::

   Dokang is extensible at the expense of the readability of the
   configuration. Balance is hard. Suggestions are welcome.


Configuration is twofold:

1. The entry point is an ``INI`` configuration file, an example of
   which is shipped with the source as ``dev.ini``. It controls both
   the configuration of the web frontend and the general settings. The
   latter are defined by ``dokang.*`` options:

   dokang.hit_limit
       The maximum number of search results to fetch. It must be a
       positive number. If equals to 0 (or if the option is omitted
       from the file), no limit is set: all results are returned.

       Default: no limit.

   dokang.index_path
       The path of the index created by the Whoosh backend. It is a
       directory that will be created on-the-fly when
       :ref:`initializing the index <cli_init>`.

   dokang.doc_sets
       The path of the second configuration file (see below) that
       lists document sets.

       To define this path, you may use ``%(here)s`` to denote the
       directory that holds the INI file.

   You may want to start from the example file and only customize
   these two values. For further details about Pyramid-related
   settings, see `the corresponding section
   <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/environment.html>`_
   as well as the `Logging
   <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/logging.html>`_
   section in the Pyramid documentation.

2. A second file (usually called ``doc_sets.py``), lists all document
   sets with their properties: title, URL, etc. It is a regular Python
   file that must define a ``DOC_SETS`` sequence, like this:

   .. code:: python

      from dokang.harvesters import sphinx_rtd_config

      DOC_SETS = (
          {'id': dokang',
           'title': "Dokang",
           'path': '/home/docs/dokang/_build/html',
           'harvester': sphinx_rtd_config(),
           'url': 'http://docs.exemple.com/dokang',
          },
      )

   Each item of ``DOC_SETS`` must be a dictionary with the following
   keys:

   id
       The id of the document set. It must be unique in ``DOC_SETS``.

   title
       The title of the document set. This title is displayed along
       search results by the command-line client and the web frontend.

   path
       The local path of the directory that holds the documents.

   harvester
       A dictionary that holds the configuration of the harvester,
       which is the component that is responsible of retrieving
       content and metadata (title) from each file. Dokang ships with
       a few utilities that provide sane values.

       See :ref:`advanced_harvester_config` in the next chapter for
       further details.

   url
       The base URL of the document set. This URL is used by the web
       frontend. Dokang does **not** serve the indexed documents, it
       provides only a link to them.

   Each text-like value should a string (in Python 3) or a unicode
   object (in Python 2).

   A sample file can be found in the source as `doc_sets.py.sample
   <https://github.com/Polyconseil/dokang/blob/master/doc_sets.py.sample>`_.

.. note::

   Having two configuration files is a bit unfortunate but it helps
   running the web frontend.


Using Dokang from the command line
----------------------------------

.. _cli_init:

Once you have created the configuration files, you must initialize the
index. You may do so with the ``init`` command of the command-line
client:

.. code:: bash

   $ dokang --settings=dev.ini init

.. note::

   If the index already exists and you would like to start from
   scratch, use the ``--force`` option to overwrite the index. The
   index will be **deleted and recreated empty**.

Providing the configuration file in every command may be
cumbersome. To work around that, you may define a ``DOKANG_SETTINGS``
environment variable and then omit the ``--settings`` option:

.. code:: bash

   $ export DOKANG_SETTINGS=/path/to/your/ini.file

You may now index documents by using the ``index`` command:

.. code:: bash

   $ dokang index

And finally search the index with the ``search`` command:

.. code:: bash

   $ dokang search needle

For further details about the arguments and options of the
command line client, see :ref:`advanced_cli_ref`.


Web frontend
------------

Dokang ships with a lightweight web frontend. The INI configuration
file described above is a valid WSGI configuration file that you may
use with your favorite WSGI server.

On a development machine, you may want to use something like
Waitress_.  First, install Waitress:

.. code:: bash

   $ pip install Waitress

Then run it:

.. code:: bash

   $ pserve dev.ini
   Starting server in PID 14135.
   serving on http://0.0.0.0:6543

See the documentation of Waitress for further details.

.. _Waitress: http://waitress.readthedocs.org
