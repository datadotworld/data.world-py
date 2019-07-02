=============
data.world-py
=============

A python library for working with data.world datasets.

This library makes it easy for data.world users to pull and work with data stored on data.world.
Additionally, the library provides convenient wrappers for data.world APIs, allowing users to create and update
datasets, add and modify files, etc, and possibly implement entire apps on top of data.world.


Quick start
===========

Install
-------

You can install it using ``pip`` directly from PyPI::

    pip install datadotworld

Optionally, you can install the library including pandas support::

    pip install datadotworld[pandas]

If you use ``conda`` to manage your python distribution, you can install from the community-maintained [conda-forge](https://conda-forge.github.io/) channel::

    conda install -c conda-forge datadotworld-py


Configure
---------

This library requires a data.world API authentication token to work.

Your authentication token can be obtained on data.world once you enable Python under
`Integrations > Python <https://data.world/integrations/python>`_

To configure the library, run the following command::

    dw configure


Alternatively, tokens can be provided via the ``DW_AUTH_TOKEN`` environment variable.
On MacOS or Unix machines, run (replacing ``<YOUR_TOKEN>>`` below with the token obtained earlier)::

    export DW_AUTH_TOKEN=<YOUR_TOKEN>

Load a dataset
--------------

The ``load_dataset()`` function facilitates maintaining copies of datasets on the local filesystem.
It will download a given dataset's `datapackage <http://specs.frictionlessdata.io/data-package/>`_
and store it under ``~/.dw/cache``. When used subsequently, ``load_dataset()`` will use the copy stored on disk and will
work offline, unless it's called with ``force_update=True`` or ``auto_update=True``. ``force_update=True`` will overwrite your local copy unconditionally. ``auto_update=True`` will only overwrite your local copy if a newer version of the dataset is available on data.world.

Once loaded, a dataset (data and metadata) can be conveniently accessed via the object returned by ``load_dataset()``.

Start by importing the ``datadotworld`` module:

.. code-block:: python

    import datadotworld as dw

Then, invoke the ``load_dataset()`` function, to download a dataset and work with it locally.
For example:

.. code-block:: python

    intro_dataset = dw.load_dataset('jonloyens/an-intro-to-dataworld-dataset')

Dataset objects allow access to data via three different properties ``raw_data``, ``tables`` and ``dataframes``.
Each of these properties is a mapping (dict) whose values are of type ``bytes``, ``list`` and ``pandas.DataFrame``,
respectively. Values are lazy loaded and cached once loaded. Their keys are the names of the files
contained in the dataset.

For example:

.. code-block:: python

    >>> intro_dataset.dataframes
    LazyLoadedDict({
        'changelog': LazyLoadedValue(<pandas.DataFrame>),
        'datadotworldbballstats': LazyLoadedValue(<pandas.DataFrame>),
        'datadotworldbballteam': LazyLoadedValue(<pandas.DataFrame>)})

**IMPORTANT**: Not all files in a dataset are tabular, therefore some will be exposed via ``raw_data`` only.

Tables are lists of rows, each represented by a mapping (dict) of column names to their respective values.

For example:

.. code-block:: python

    >>> stats_table = intro_dataset.tables['datadotworldbballstats']
    >>> stats_table[0]
    OrderedDict([('Name', 'Jon'),
                 ('PointsPerGame', Decimal('20.4')),
                 ('AssistsPerGame', Decimal('1.3'))])

You can also review the metadata associated with a file or the entire dataset, using the ``describe`` function.
For example:

.. code-block:: python

    >>> intro_dataset.describe()
    {'homepage': 'https://data.world/jonloyens/an-intro-to-dataworld-dataset',
     'name': 'jonloyens_an-intro-to-dataworld-dataset',
     'resources': [{'format': 'csv',
       'name': 'changelog',
       'path': 'data/ChangeLog.csv'},
      {'format': 'csv',
       'name': 'datadotworldbballstats',
       'path': 'data/DataDotWorldBBallStats.csv'},
      {'format': 'csv',
       'name': 'datadotworldbballteam',
       'path': 'data/DataDotWorldBBallTeam.csv'}]}
    >>> intro_dataset.describe('datadotworldbballstats')
    {'format': 'csv',
     'name': 'datadotworldbballstats',
     'path': 'data/DataDotWorldBBallStats.csv',
     'schema': {'fields': [{'name': 'Name', 'title': 'Name', 'type': 'string'},
                           {'name': 'PointsPerGame',
                            'title': 'PointsPerGame',
                            'type': 'number'},
                           {'name': 'AssistsPerGame',
                            'title': 'AssistsPerGame',
                            'type': 'number'}]}}

Query a dataset
---------------

The ``query()`` function allows datasets to be queried live using ``SQL`` or ``SPARQL`` query languages.

To query a dataset, invoke the ``query()`` function.
For example:

.. code-block:: python

    results = dw.query('jonloyens/an-intro-to-dataworld-dataset', 'SELECT * FROM DataDotWorldBBallStats')

Query result objects allow access to the data via ``raw_data``, ``table`` and ``dataframe`` properties, of type
``json``, ``list`` and ``pandas.DataFrame``, respectively.

For example:

.. code-block:: python

    >>> results.dataframe
          Name  PointsPerGame  AssistsPerGame
    0      Jon           20.4             1.3
    1      Rob           15.5             8.0
    2   Sharon           30.1            11.2
    3     Alex            8.2             0.5
    4  Rebecca           12.3            17.0
    5   Ariane           18.1             3.0
    6    Bryon           16.0             8.5
    7     Matt           13.0             2.1


Tables are lists of rows, each represented by a mapping (dict) of column names to their respective values.
For example:

.. code-block:: python

    >>> results.table[0]
    OrderedDict([('Name', 'Jon'),
                 ('PointsPerGame', Decimal('20.4')),
                 ('AssistsPerGame', Decimal('1.3'))])

To query using ``SPARQL`` invoke ``query()`` using ``query_type='sparql'``, or else, it will assume
the query to be a ``SQL`` query.

Just like in the dataset case, you can view the metadata associated with a query result using the ``describe()``
function.

For example:

.. code-block:: python

    >>> results.describe()
    {'fields': [{'name': 'Name', 'type': 'string'},
                {'name': 'PointsPerGame', 'type': 'number'},
                {'name': 'AssistsPerGame', 'type': 'number'}]}

Work with files
---------------

The ``open_remote_file()`` function allows you to write data to or read data from a file in a
data.world dataset.

Writing files
.............

The object that is returned from the ``open_remote_file()`` call is similar to a file handle that
would be used to write to a local file - it has a ``write()`` method, and contents sent to that
method will be written to the file remotely.

.. code-block:: python

        >>> import datadotworld as dw
        >>>
        >>> with dw.open_remote_file('username/test-dataset', 'test.txt') as w:
        ...   w.write("this is a test.")
        >>>

Of course, writing a text file isn't the primary use case for data.world - you want to write your
data!  The return object from ``open_remote_file()`` should be usable anywhere you could normally
use a local file handle in write mode - so you can use it to serialize the contents of a PANDAS
``DataFrame`` to a CSV file...

.. code-block:: python

        >>> import pandas as pd
        >>> df = pd.DataFrame({'foo':[1,2,3,4],'bar':['a','b','c','d']})
        >>> with dw.open_remote_file('username/test-dataset', 'dataframe.csv') as w:
        ...   df.to_csv(w, index=False)

Or, to write a series of ``dict`` objects as a JSON Lines file...

.. code-block:: python

        >>> import json
        >>> with dw.open_remote_file('username/test-dataset', 'test.jsonl') as w:
        ...   json.dump({'foo':42, 'bar':"A"}, w)
        ...   json.dump({'foo':13, 'bar':"B"}, w)
        >>>

Or to write a series of ``dict`` objects as a CSV...

.. code-block:: python

        >>> import csv
        >>> with dw.open_remote_file('username/test-dataset', 'test.csv') as w:
        ...   csvw = csv.DictWriter(w, fieldnames=['foo', 'bar'])
        ...   csvw.writeheader()
        ...   csvw.writerow({'foo':42, 'bar':"A"})
        ...   csvw.writerow({'foo':13, 'bar':"B"})
        >>>

And finally, you can write binary data by streaming ``bytes`` or ``bytearray`` objects, if you open the
file in binary mode...

.. code-block:: python

        >>> with dw.open_remote_file('username/test-dataset', 'test.txt', mode='wb') as w:
        ...   w.write(bytes([100,97,116,97,46,119,111,114,108,100]))

Reading files
.............

You can also read data from a file in a similar fashion

.. code-block:: python

        >>> with dw.open_remote_file('username/test-dataset', 'test.txt', mode='r') as r:
        ...   print(r.read)


Reading from the file into common parsing libraries works naturally, too - when opened in 'r' mode, the
file object acts as an Iterator of the lines in the file:

.. code-block:: python

        >>> with dw.open_remote_file('username/test-dataset', 'test.txt', mode='r') as r:
        ...   csvr = csv.DictReader(r)
        ...   for row in csvr:
        ...      print(row['column a'], row['column b'])


Reading binary files works naturally, too - when opened in 'rb' mode, ``read()`` returns the contents of
the file as a byte array, and the file object acts as an iterator of bytes:

.. code-block:: python

        >>> with dw.open_remote_file('username/test-dataset', 'test', mode='rb') as r:
        ...   bytes = r.read()


Additional API Features
-----------------------

For a complete list of available API operations, see
`official documentation <https://docs.data.world/documentation/api/>`_.

Python wrappers are implemented by the ``ApiClient`` class. To obtain an instance, simply call ``api_client``.
For example:

.. code-block:: python

    client = dw.api_client

The client currently implements the following functions:

* ``create_dataset``
* ``update_dataset``
* ``replace_dataset``
* ``get_dataset``
* ``delete_dataset``
* ``add_files_via_url``
* ``append_records``
* ``upload_files``
* ``upload_file``
* ``delete_files``
* ``sync_files``
* ``download_dataset``
* ``download_file``
* ``get_user_data``
* ``fetch_contributing_datasets``
* ``fetch_liked_datasets``
* ``fetch_datasets``
* ``fetch_contributing_projects``
* ``fetch_liked_projects``
* ``fetch_projects``
* ``get_project``
* ``create_project``
* ``update_project``
* ``replace_project``
* ``add_linked_dataset``
* ``remove_linked_dataset``
* ``delete_project``
* ``get_insight``
* ``get_insights_for_project``
* ``create_insight``
* ``replace_insight``
* ``update_insight``
* ``delete_insight``

For a few examples of what the ``ApiClient`` can be used for, see below.

Add files from URL
..................

The ``add_files_via_url()`` function can be used to add files to a dataset from a URL. 
This can be done by specifying ``files`` as a dictionary where the keys are the desired file name and each item is an object containing ``url``, ``description`` and ``labels``. 

For example:

.. code-block:: python

    >>> client = dw.api_client
    >>> client.add_files_via_url('username/test-dataset', files={'sample.xls': {'url':'http://www.sample.com/sample.xls', 'description': 'sample doc', 'labels': ['raw data']}})

Append records to stream
........................

The ``append_record()`` function allows you to append JSON data to a data stream associated with a dataset. Streams do not need to be created in advance. Streams are automatically created the first time a ``streamId`` is used in an append operation. 

For example:

.. code-block:: python

    >>> client = dw.api_client
    >>> client.append_records('username/test-dataset','streamId', {'data': 'data'})

Contents of a stream will appear as part of the respective dataset as a .jsonl file.

You can find more about those functions using ``help(client)``

