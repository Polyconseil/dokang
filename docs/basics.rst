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

The entry point is an ``INI`` configuration file, an example of
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

dokang.uploaded_docs.dir
    The path where HTML documentation is uploaded.

    To define this path, you may use ``%(here)s`` to denote the
    directory that holds the INI file.

dokang.uploaded_docs.token
    The identification token used to allow documentation upload.

dokang.uploaded_docs.harvester
    The harvester to use for all projects (fully qualified class name).

You may want to start from the example file and only customize
these five values. For further details about Pyramid-related
settings, see `the corresponding section
<http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/environment.html>`_
as well as the `Logging
<http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/logging.html>`_
section in the Pyramid documentation.


Upload and index documentation
------------------------------

Supposing you have a running Dokang instance on http://dokang.example.com,
and you want to upload the documentation of your project, you need to:

- zip the documentation (your zip file must have a top-level index.html);
- post your documentation on http://dokang.example.com/upload/ using ``multipart/form-data`` content type and
  the following fields:

  - ``:action`` with value  ``doc_upload``
  - ``name`` with project name
  - ``content`` with the zipfile

.. code-block:: bash

    $ cd project_html_built_doc/
    $ 7z a ../documentation.zip .
    $ curl -X POST --form name=project_name -F ":action=doc_upload" -F content=@../documentation.zip http://dokang:my-secret-token@dokang.example.com/upload


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
