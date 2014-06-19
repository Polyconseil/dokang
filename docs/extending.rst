Extending Dokang
================

Dokang currently supports a single backend: Whoosh. Whoosh is
responsible of the indexation and the actual search. As of now, Dokang
does not let you easily use another backend such as Elasticsearch.
Contributions are welcome.

However, you may want to add your own harvester. The harvester is
responsible to retrieve data (title and content) from a document.
Dokang provides a few harvesters but you may implement your own.

An harvester should be a subclass of ``dokang.harvesters.Harvester``
and implement an ``harvest_file(path)`` method that should return a
dictionary with the following keys. All values should be text-like: a
string (in Python 3) or a unicode object (in Python 2).

title
    The title of the document.

content
    The concatenated content of the document.

kind
    The kind of document: HTML, PDF, etc.


Here is an example of a simple harvester for text files.

.. code:: python

   import codecs
   import os

   from dokang.harvesters import Harvester

   class TextHarvester(Harvester):

       def harvest_file(path):
           with codecs.open(path, encoding='utf-8') as fp:
               return {
                   'title': os.path.basename(path),  # Use the filename as the title
                   'content: 'fp.read()',
                   'kind': 'TXT',
               }

You may then use it in your configuration file, like this:

.. code:: python

   DOC_SETS = (
    {'harvester': {
       '.txt': TextHarvester},
     # [...]
    }
