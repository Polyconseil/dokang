Change log
==========

0.9.4 (2016-07-05)
------------------

- fix dockerfile.


0.9.3 (2016-07-04)
------------------

- Add dockerfile.


0.9.2 (2016-04-26)
------------------

- Keep title when updating documentation.


0.9.1 (2016-04-01)
------------------

- Fix packaging


0.9.0 (2016-04-01)
------------------

- Allow running simultaneous threads of Dokang web application.

  Until now, Dokang updated its list of document sets at startup and
  when a new document set was uploaded. Running multiple threads of
  the web application was obviously not working great, as one thread
  would not see any new document set if it was added by another
  thread.

  This limitation has now been lifted and Dokang web application can
  run with multiple threads (for example with multiple uWSGI workers).


Dokang 0.8.2 (2016-02-24)
-------------------------

- Update doc set title after uploading a new version of the documentation.


Dokang 0.8.1 (2016-02-24)
-------------------------

- Fix packaging.


Dokang 0.8.0 (2016-02-24)
-------------------------

- Use the title of the index page as the title of each doc set.
- Group doc sets by the first letter of their title.

Dokang 0.7.0 (2016-02-01)
-------------------------

- Add support of Python 3.5.

- When initializing the index, ``dokang init`` now creates all needed
  intermediate-level directories.

- Add purge option to ``dokang clear`` to delete uploaded files.

- Fix change detection: we used to store and use the modification time
  of the files. We now compute and store an MD5 hash for each file. It
  is slower than getting the modification time, but it handles more
  use cases.

  **This is a backward-incompatible change.** You must reindex all
  documents, like this::

      dokang init --force
      dokang index

- Remove bogus indexation optimization. The indexation should be a lot
  faster now, especially on large document base.

- Fix encoding error when parsing non ASCII, non UTF-8 HTML files.
  UTF-8 files were correctly processed, though.

- Add basic support for OpenSearch.

- Exclude more Sphinx-generated files like ``objects.inv`` and
  ``searchindex.js``.

- Display path of files in the search results of the command line
  client.

- Fix bug in document deletion. When a document was detected as
  deleted from a document set (i.e. when a file was not present
  anymore in the "upload" directory), the indexation process deleted
  from the index *all* documents with the same path (for example
  ``index.html``) in *all* document sets. The files themselves were
  not deleted so the next indexation would add them back to the index.

- Use an asynchronous index writer that allows multiple indexation to
  be done concurrently. Without this, a ``whoosh.index.LockError``
  exception is raised.


Dokang 0.6.1 (2015-03-03)
-------------------------

- Fix redirection error when uploading documentation.


Dokang 0.6.0 (2015-03-03)
-------------------------

**Brown bag release.**

- Drop Python 2.6 support.

- Make documentation available from the root of Dokang ("/"). This
  change is backward-incompatible.

  Before this commit, if the upload dir was named "uploaded", the
  documentation would be available at ``/uploaded/<doc_set_id>``. This
  was a bit too verbose.

  With this (backward-incompatible) change, the documentation is now
  available at ``/<doc_set_id>``.


Dokang 0.5.0 (2015-02-18)
-------------------------

- Add "highlight" in the query string of the URLs of search results.
  This parameter is understood by Sphinx-generated HTML files.

- Add documentation uploading end point (to use Dokang web frontend to serve the documentation)


Dokang 0.4.2 (2014-09-01)
-------------------------

- Fix bad-looking (but working) URLs generated in the web front-end.
  They used to contain two consecutive slashes (for example
  http://example.com/project//doc.html) when the configuration of the
  project had a slash at the end of its URL.


Dokang 0.4.1 (2014-08-27)
-------------------------

- Fixed MANIFEST.in so that the Python package contains all templates
  and stylesheets required by the web front-end.


Dokang 0.4.0 (2014-07-04)
-------------------------

- A new ``dokang.hit_limit`` option has been added to the INI
  configuration file. It limits the number of results shown on the web
  front-end (or lifts this limit if the option is absent).


Dokang 0.3.0 (2014-07-04)
-------------------------

- Fix bug in the HTML harvester. Trying to use it would fail with an
  exception because Whoosh would complain about something that
  unexpectedly is a byte string.

- Fix bug in the handling of deleted documents. They were not deleted
  from the index.


Dokang 0.2.0 (2014-06-24)
-------------------------

Initial version.
