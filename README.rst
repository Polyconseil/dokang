.. Edit with care, this file is included in the documentation.

Dokang
######

Dokang is a lightweight documentation repository. It is a web
application that:

1. Provides an endpoint for clients to upload their documentation.

   Sending documentation to Dokang is as simple as issuing a POST
   query such as:

   .. code:: bash

       $ curl \
         -X POST \
         --form name=project_name \
         -F ":action=doc_upload" \
         -F content=@../documentation.zip \
         http://dokang:my-secret-token@dokang.example.com/upload

2. Serves a home page with a list of all documentations and a simple
   search form that lets users search in HTML, text and PDF
   files. Other formats can be handled through the use of extensions.

3. Serves all documentations.

Dokang also comes with a command line interface. It is lightweight in
the sense that it is merely a wrapper around the Whoosh search engine
with a very simple HTML text indexer. It can be extended to retrieve
content from other types of files (such as PDF).

Dokang is similar to Readthedocs (although Readthedocs has a much
broader set of features) but provides a global search across all
hosted documentations. All of this is provided with a simple setup
that does not need any relational database.

We (`Polyconseil`_) use it to search through the `Sphinx
<http://sphinx-doc.org/>`_-generated documentation of all our
projects. However, it may be used to host any kind of documentation.

.. _Polyconseil: https://www.polyconseil.fr/


Build and run your own docker image
-----------------------------------

To build your own image:

.. code:: bash

    $ docker build -t dokang .

To run the image:

.. code:: bash

    $ docker run --rm -e DOKANG_UPLOAD_TOKEN=my_little_secret \
      -e DOKANG_NAME='My docs' \
      -e DOKANG_DESCRIPTION='Documentations of all my projects' \
      -e DOKANG_SERVER_TRUSTED_PROXY=129.14.12.1  # Optional: the IP address of the proxy to pass to waitress server's trusted_proxy
      -p 8080:6543
      dokang

Go to http://localhost:8080/ in your browser, you should see the list of documentations.
