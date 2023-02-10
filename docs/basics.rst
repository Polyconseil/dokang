Basics
======

In this chapter, we will skim over the installation and configuration
to search in the documentation of Dokang itself.


Concepts
--------

A *document set* represents a single documentation, i.e. a set of
related documents (files) that resides in a directory and its
sub-directories, for example this documentation of Dokang. You may
instruct Dokang to index one or more document sets, and then search in
all sets or only one.

A *harvester* extracts content from a file: a list of words and a few
metadata, like the title.


Installation
------------

Dokang is compatible with Python 3 only (>= 3.7).

In a brand new virtual environment, install with:

.. code:: bash

    pip install Dokang

If you have cloned the `Git repository`_, use this instead:

.. code:: bash

    pip install -e .


.. _Git repository: https://github.com/Polyconseil/Dokang


.. _basics_configuration:

Configuration
-------------

The entry point is an ``INI`` configuration file, an example of which
is shipped with the source as `dev.ini`_. It controls both the
configuration of the web frontend and general settings. The latter are
defined by ``dokang.*`` options:

.. _dev.ini: https://github.com/Polyconseil/dokang/blob/master/dev.ini

dokang.hit_limit
   The maximum number of search results to fetch. It must be a
   positive number. If equals to 0 (or if the option is omitted
   from the file), no limit is set: all results are returned.

   Default: no limit.

dokang.index_path
    The path of the index created by the Whoosh backend. It is a
    directory that will be created on-the-fly when
    :ref:`the index is initialized <cli_init>`.

dokang.uploaded_docs.dir
    The path where HTML documentation is uploaded.

    To define this path, you may use ``%(here)s`` to denote the
    directory that holds the INI file.

dokang.uploaded_docs.token
    The identification token used to allow documentation upload.

dokang.uploaded_docs.harvester
    The harvester to use for all projects (fully qualified Python
    class name).

dokang.opensearch.name
    The name of your documentation repository, for OpenSearch (see
    :ref:`below <opensearch>`).

dokang.opensearch.name
    A description of your documentation repository, for OpenSearch (see
    :ref:`below <opensearch>`).

You may want to start from the example file and only customize these
values. For further details about Pyramid-related settings, see `the
corresponding section
<http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/environment.html>`_
as well as the `Logging
<http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/logging.html>`_
section in the Pyramid documentation.


Initializing the index
----------------------

.. _cli_init:

Once you have created the configuration file, you must initialize the
search index. You may do so with the ``init`` command of the
command-line client:

.. code:: bash

   $ dokang --settings=dev.ini init

.. note::

   If the index already exists and you would like to start from
   scratch, use the ``--force`` option to overwrite the index. The
   index will be **deleted and recreated empty**.

For further details about the arguments and options of the
command line client, see :ref:`advanced_cli_ref`.


Starting Dokang
---------------

The INI configuration file described above is a valid WSGI
configuration file that you may use with your favorite WSGI server.

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

.. _Waitress: http://waitress.readthedocs.io


Upload and index documentation
------------------------------

If you visit http://localhost:6543 in a web browser, the page will be
quite empty. Let's upload the documentation of a project:

- zip the documentation (your ZIP file must have a top-level
  "index.html");
- post your documentation on http://localhost:6543/upload/ using
  ``multipart/form-data`` content type and the following fields:

  - ``:action``, must be ``doc_upload``,
  - ``name``, the name of your project,
  - ``content``, the ZIP file.

.. code-block:: bash

    $ cd project_html_doc/
    $ 7z a ../documentation.zip .
    $ curl -X POST \
           --form name=project_name \
           -F ":action=doc_upload" \
           -F content=@../documentation.zip \
           http://dokang:my-secret-token@localhost:6543/upload

You should see a success message. If you refresh
http://localhost:6543/ in your web browser, you should now be able to
search and find terms that appear in the documentation you have
uploaded.


.. _opensearch:

OpenSearch
----------

Dokang has basic support for OpenSearch. That means that you can set
up an instance of Dokang as a custom search source (like Google and
Wikipedia in Firefox).
