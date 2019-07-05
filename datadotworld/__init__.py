# data.world-py
# Copyright 2017 data.world, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
#
# This product includes software developed at
# data.world, Inc.(http://data.world/).


"""
A python library for working with data.world datasets

"""

from __future__ import absolute_import

import weakref

from datadotworld.config import (
    FileConfig,
    ChainedConfig,
    InlineConfig,
    EnvConfig
)
from datadotworld.datadotworld import DataDotWorld, UriParam  # noqa: F401

__version__ = '1.7.0'

# Convenience top-level functions

__instances = weakref.WeakValueDictionary()


def _get_instance(profile, **kwargs):
    """

    :param profile:

    """
    instance = __instances.get(profile)

    if instance is None:
        config_param = (ChainedConfig(config_chain=[
            InlineConfig(kwargs.get('auth_token')),
            EnvConfig(),
            FileConfig()])
                if profile == 'default'
                else FileConfig(profile=profile))
        instance = DataDotWorld(config=config_param)
        __instances[profile] = instance
    return instance


def load_dataset(dataset_key, force_update=False, auto_update=False,
                 profile='default', **kwargs):
    """Load a dataset from the local filesystem, downloading it from data.world
    first, if necessary.

    This function returns an object of type `LocalDataset`. The object
    allows access to metedata via it's `describe()` method and to all the data
    via three properties `raw_data`, `tables` and `dataframes`, all of which
    are mappings (dict-like structures).

    :param dataset_key: Dataset identifier, in the form of owner/id or of a url
    :type dataset_key: str
    :param force_update: Flag, indicating if a new copy of the dataset should
        be downloaded replacing any previously downloaded copy
        (Default value = False)
    :type force_update: bool
    :param auto_update: Flag, indicating that dataset be updated to the latest
        version
    :type auto_update: bool
    :param profile: Configuration profile (account) to use.
        (Default value = 'default')
    :type profile: str, optional
    :returns: The object representing the dataset
    :rtype: LocalDataset
    :raises RestApiError: If a server error occurs

    Examples
    --------
    >>> import datadotworld as dw
    >>> dataset = dw.load_dataset('jonloyens/an-intro-to-dataworld-dataset')
    >>> list(dataset.dataframes)
    ['changelog', 'datadotworldbballstats', 'datadotworldbballteam']
    """
    return _get_instance(profile, **kwargs). \
        load_dataset(dataset_key,
                     force_update=force_update,
                     auto_update=auto_update)


def query(dataset_key, query, query_type='sql', profile='default',
          parameters=None, **kwargs):
    """Query an existing dataset

    :param dataset_key: Dataset identifier, in the form of owner/id or of a url
    :type dataset_key: str
    :param query: SQL or SPARQL query
    :type query: str
    :param query_type: The type of the query. Must be either 'sql' or 'sparql'.
        (Default value = 'sql')
    :type query_type: {'sql', 'sparql'}, optional
    :param parameters: parameters to the query - if SPARQL query, this should
        be a dict containing named parameters, if SQL query, then this should
        be a list containing positional parameters.  Boolean values will be
        converted to xsd:boolean, Integer values to xsd:integer, and other
        Numeric values to xsd:decimal. anything else is treated as a String
        literal (Default value = None)
    :type parameters: query parameters, optional
    :param profile: Configuration profile (account) to use.
        (Default value = 'default')
    :type profile: str, optional
    :returns: Object containing the results of the query
    :rtype: Results
    :raises RuntimeError: If a server error occurs

    Examples
    --------
    >>> import datadotworld as dw
    >>> results = dw.query(
    ...     'jonloyens/an-intro-to-dataworld-dataset',
    ...     'SELECT * FROM `DataDotWorldBBallStats`, `DataDotWorldBBallTeam` '
    ...     'WHERE DataDotWorldBBallTeam.Name = DataDotWorldBBallStats.Name')
    >>> df = results.dataframe
    >>> df.shape
    (8, 6)
    """
    return _get_instance(profile, **kwargs).query(dataset_key, query,
                                                  query_type=query_type,
                                                  parameters=parameters,
                                                  **kwargs)


def open_remote_file(dataset_key, file_name, profile='default',
                     mode='w', **kwargs):
    """Open a remote file object that can be used to write to or read from
    a file in a data.world dataset

    :param dataset_key: Dataset identifier, in the form of owner/id
    :type dataset_key: str
    :param file_name: The name of the file to open
    :type file_name: str
    :param mode: the mode for the file - must be 'w', 'wb', 'r', or 'rb' -
        indicating read/write ('r'/'w') and optionally "binary"
        handling of the file data. (Default value = 'w')
    :type mode: str, optional
    :param chunk_size: size of chunked bytes to return when reading streamed
        bytes in 'rb' mode
    :type chunk_size: int, optional
    :param decode_unicode: whether to decode textual responses as unicode when
        returning streamed lines in 'r' mode
    :type decode_unicode: bool, optional
    :param profile:  (Default value = 'default')
    :param **kwargs:

    Examples
    --------
    >>> import datadotworld as dw
    >>>
    >>> # write a text file
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'test.txt') as w:
    ...   w.write("this is a test.")
    >>>
    >>> # write a jsonlines file
    >>> import json
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'test.jsonl') as w:
    ...   json.dump({'foo':42, 'bar':"A"}, w)
    ...   w.write("\\n")
    ...   json.dump({'foo':13, 'bar':"B"}, w)
    ...   w.write("\\n")
    >>>
    >>> # write a csv file
    >>> import csv
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'test.csv') as w:
    ...   csvw = csv.DictWriter(w, fieldnames=['foo', 'bar'])
    ...   csvw.writeheader()
    ...   csvw.writerow({'foo':42, 'bar':"A"})
    ...   csvw.writerow({'foo':13, 'bar':"B"})
    >>>
    >>> # write a pandas dataframe as a csv file
    >>> import pandas as pd
    >>> df = pd.DataFrame({'foo':[1,2,3,4],'bar':['a','b','c','d']})
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'dataframe.csv') as w:
    ...   df.to_csv(w, index=False)
    >>>
    >>> # write a binary file
    >>> with dw.open_remote_file('username/test-dataset',
    >>>                          'test.txt', mode='wb') as w:
    ...   w.write(bytes([100,97,116,97,46,119,111,114,108,100]))
    >>>
    >>> # read a text file
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'test.txt', mode='r') as r:
    ...   print(r.read())
    >>>
    >>> # read a csv file
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'test.csv', mode='r') as r:
    ...   csvr = csv.DictReader(r)
    ...   for row in csvr:
    ...      print(row['column a'], row['column b'])
    >>>
    >>> # read a binary file
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'test', mode='rb') as r:
    ...   bytes = r.read()
    """
    return _get_instance(profile, **kwargs).open_remote_file(
        dataset_key, file_name,
        mode=mode, **kwargs)


def api_client(profile='default', **kwargs):
    """Return API client for access to data.world's REST API

    :param profile: Configuration profile (account) to use.
        (Default value = 'default')
    :type profile: str, optional
    :returns: REST API client object
    :rtype: RestApiClient

    Examples
    --------
    >>> import datadotworld as dw
    >>> client = dw.api_client()
    >>> client.get_dataset(
    ...     'jonloyens/an-intro-to-dataworld-dataset').get('title')
    'An Intro to data.world Dataset'
    """
    return _get_instance(profile, **kwargs).api_client


if __name__ == "__main__":
    import doctest

    doctest.testmod()
