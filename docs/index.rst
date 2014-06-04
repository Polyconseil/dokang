Dokang
======

Dokang is a lightweight search engine for HTML documents. It comes
with a command-line program and a web frontend.

It is lightweight in the sense that it is merely a wrapper around the
Whoosh search engine, with a very simple HTML text indexer that is
tailored for Sphinx documentations.

A key concept in Dokang is the "document set". A document set
represents a set of related documents, for example the documentation
of a single project. You may instruct Dokang to index one or more
document sets, and then search in all or only a single set. It's so
new and brilliant that I am going to trademark and patent all this.


Installation
------------

In a brand new virtual environment, install with ``pip install
Dokang``, or ``pip install -r requirements.txt`` if you have cloned
the Git repository.


Configuration
-------------

Configuration is twofold:

1. The entry point is an ``INI`` configuration file, an example of
   which is shipped with the source as ``dev.ini``. It control both
   the configuration of the web frontend and the general settings. The
   latter are defined by ``dokang.*`` options:

   dokang.index_path
       The path of the index created by the Whoosh backend. It is a
       directory that will be created on-the-fly when
       :ref:`initializing the index <cli_init>`.

   dokang.doc_sets
       The path of the second configuration file (see below) that
       lists document sets.

       To define this path, you may use ``%(here)s`` to denote the
       directory that holds the INI file.

2. A second file that may be called ``doc_sets.py``, lists all
   document sets with their properties: title, URL, etc. A sample file
   can be found in the source a ``doc_sets.py.sample``. It is a Python
   file that must define a ``DOC_SETS`` dictionary, like this:

   .. code:: python

      DOC_SETS = {
          u'dokang': {
              'path': '/home/docs/dokang/_build/html',
              'url': 'http://docs.exemple.com/dokang',
              'title': "Dokang"
          },
      }

   Each key of ``DOC_SETS`` must be a unicode object (under Python 2)
   or a string (under Python 3), not bytes. Each entry in the
   ``DOC_SETS`` dictionary is itself a dictionary that represents a
   document set. It should have the following keys:

   path
       The local path of the directory that holds the documents.

   title
       The title of the document set. This title is displayed along
       search results by the command-line client and the web frontend.

   url
       The base URL of the document set. This URL is used by the web
       frontend. Dokang does **not** serve the indexed documents, it
       provides only a link to them.

.. note::

   Having two configuration files is a bit unfortunate but it helps
   running the web frontend.


Usage
-----

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

You may then search the index with the ``search`` command:

.. code:: bash

   $ dokang search needle

.. note::

   Use ``dokang --help`` to see a list of commands and general
   options. Use ``dokang <command> --help`` to get help and a list of
   options of a specific command.


Web frontend
------------

Dokang ships with a lightweight web frontend. The INI configuration
file described above is a valid WSGI configuration file that you may
use with your favorite WSGI server.

On a development machine, you may want to use something like
Waitress_.  First, you need to install it:

.. code:: bash

   $ pip install Waitress

Then run it:

.. code:: bash

   $ pserve dev.ini
   Starting server in PID 14135.
   serving on http://0.0.0.0:6543

See the documentation of Waitress for further details.

.. _Waitress: http://waitress.readthedocs.org
