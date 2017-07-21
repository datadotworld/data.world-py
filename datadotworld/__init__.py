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

from datadotworld.config import FileConfig, ChainedConfig
from datadotworld.datadotworld import DataDotWorld

__version__ = '1.3.0'

# Convenience top-level functions

__instances = weakref.WeakValueDictionary()


def _get_instance(profile):
    instance = __instances.get(profile)
    if instance is None:
        config_param = (ChainedConfig()
                        if profile == 'default'
                        else FileConfig(profile=profile))
        instance = DataDotWorld(config=config_param)
        __instances[profile] = instance
    return instance


def load_dataset(dataset_key, force_update=False, profile='default'):
    """
    Load a dataset from the local filesystem, downloading it from data.world
    first, if necessary.

    This function returns an object of type `LocalDataset`. The object
    allows access to metedata via it's `describe()` method and to all the data
    via three properties `raw_data`, `tables` and `dataframes`, all of which
    are mappings (dict-like structures).


    Parameters
    ----------
    dataset_key : str
        Dataset identifier, in the form of owner/id or of a url
    force_update : bool
        Flag, indicating if a new copy of the dataset should be downloaded
        replacing any previously downloaded copy
    profile : str, optional
        Configuration profile (account) to use.

    Returns
    -------
    LocalDataset
        The object representing the dataset

    Raises
    ------
    RestApiError
        If a server error occurs

    Examples
    --------
    >>> import datadotworld as dw
    >>> dataset = dw.load_dataset('jonloyens/an-intro-to-dataworld-dataset')
    >>> list(dataset.dataframes)
    ['changelog', 'datadotworldbballstats', 'datadotworldbballteam']
    """
    return _get_instance(profile).load_dataset(dataset_key,
                                               force_update=force_update)


def query(dataset_key, query, query_type='sql', profile='default',
          parameters=None):
    """Query an existing dataset

    Parameters
    ----------
    dataset_key : str
        Dataset identifier, in the form of owner/id or of a url
    query : str
        SQL or SPARQL query
    query_type : {'sql', 'sparql'}, optional
        The type of the query. Must be either 'sql' or 'sparql'.
    parameters: query parameters, optional
        parameters to the query - if SPARQL query, this should be a dict
        containing named parameters, if SQL query, then this should be a
        list containing positional parameters.  Boolean values will be
        converted to xsd:boolean, Integer values to xsd:integer, and other
        Numeric values to xsd:decimal. anything else is treated as a String
        literal
    profile : str, optional
        Configuration profile (account) to use.

    Returns
    -------
    Results
        Object containing the results of the query

    Raises
    ------
    RuntimeError
        If a server error occurs

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
    return _get_instance(profile).query(dataset_key, query,
                                        query_type=query_type,
                                        parameters=parameters)


def open_remote_file(dataset_key, file_name, profile='default',
                     mode='w'):
    """
    Open a remote file object that can be used to write to a file in a
    data.world dataset

    Parameters
    ----------
    dataset_key : str
        Dataset identifier, in the form of owner/id
    file_name: str
        The name of the file to write
    profile : str, optional
        Configuration profile (account) to use.
    mode: str, optional
        the mode for the file - currently only 'w' (write string) or
        'wb' (write binary) are supported, any other value will throw
        an exception

    Examples
    --------
    >>> import datadotworld as dw
    >>>
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'test.txt') as w:
    ...   w.write("this is a test.")
    >>>
    >>> import json
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'test.jsonl') as w:
    ...   json.dump({'foo':42, 'bar':"A"}, w)
    ...   json.dump({'foo':13, 'bar':"B"}, w)
    >>>
    >>> import csv
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'test.csv') as w:
    ...   csvw = csv.DictWriter(w, fieldnames=['foo', 'bar'])
    ...   csvw.writeheader()
    ...   csvw.writerow({'foo':42, 'bar':"A"})
    ...   csvw.writerow({'foo':13, 'bar':"B"})
    >>>
    >>> import pandas as pd
    >>> df = pd.DataFrame({'foo':[1,2,3,4],'bar':['a','b','c','d']})
    >>> with dw.open_remote_file('username/test-dataset',
    ...                          'dataframe.csv') as w:
    ...   df.to_csv(w, index=False)
    >>>
    >>> with dw.open_remote_file('username/test-dataset',
    >>>                          'test.txt', mode='wb') as w:
    ...   w.write(bytes([100,97,116,97,46,119,111,114,108,100]))
    """
    return _get_instance(profile).open_remote_file(
        dataset_key, file_name, mode)


def api_client(profile='default'):
    """Return API client for access to data.world's REST API

    Parameters
    ----------
    profile : str, optional
        Configuration profile (account) to use.

    Returns
    -------
    RestApiClient
        REST API client object

    Examples
    --------
    >>> import datadotworld as dw
    >>> client = dw.api_client()
    >>> client.get_dataset(
    ...     'jonloyens/an-intro-to-dataworld-dataset').get('title')
    'An Intro to data.world Dataset'
    """
    return _get_instance(profile).api_client


if __name__ == "__main__":
    import doctest

    doctest.testmod()
