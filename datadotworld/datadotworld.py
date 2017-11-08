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

from __future__ import absolute_import

import shutil
from datetime import datetime
from os import path
from warnings import warn, filterwarnings
import numbers

import requests

from datadotworld.client.api import RestApiClient, RestApiError
from datadotworld.config import ChainedConfig
from datadotworld.models.dataset import LocalDataset
from datadotworld.models.query import QueryResults
from datadotworld.util import _user_agent, parse_dataset_key
from datadotworld.files import RemoteFile


class DataDotWorld(object):
    """Facade with main features of datadotworld package

    .. note:: In most cases, directly instantiating this class is unnecessary.
              All functions are conveniently wrapped and exposed at the
              `datadotworld` package level.

    Parameters
    ----------
    profile : str, optional
        Configuration profile (account) to use

    Attributes
    ----------
    api_client
        REST API client object
    """

    def __init__(self, config=None):
        self._protocol = 'https'
        self._query_host = 'query.data.world'
        self._download_host = 'download.data.world'

        self._config = config or ChainedConfig()
        self.api_client = RestApiClient(self._config)

    def query(self, dataset_key, query, query_type="sql", parameters=None):
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

        Returns
        -------
        Results
            Object containing the results of the query

        Raises
        ------
        RuntimeError
            If a server error occurs
        """
        # TODO Move network request to RestApiClient
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        params = {
            "query": query
        }
        if parameters and query_type == "sparql":
            # if SPARQL, then the parameters should be a Mapping containing
            # named parameters
            params["parameters"] = ",".join(
                ["{}={}".format(k, convert_to_sparql_literal(parameters[k]))
                 for k in parameters.keys()])
        elif parameters and query_type == "sql":
            # if SQL, then the parameters should be an array with positional
            # parameters, need to unwind them to $data_world_paramN for each
            # 0-indexed position N
            parameters = {"$data_world_param{}".format(i): x
                          for i, x in enumerate(parameters)}
            params["parameters"] = ",".join(["{}={}".format(
                k, convert_to_sparql_literal(parameters[k]))
                for k in parameters.keys()])
        url = "{0}://{1}/{2}/{3}/{4}".format(self._protocol, self._query_host,
                                             query_type, owner_id, dataset_id)
        headers = {
            'User-Agent': _user_agent(),
            'Accept': 'application/sparql-results+json',
            'Authorization': 'Bearer {0}'.format(self._config.auth_token)
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return QueryResults(response.json())
        raise RuntimeError(
            'Error executing query: {}'.format(response.content))

    def load_dataset(self, dataset_key, force_update=False, auto_update=False):
        """
        Load a dataset from the local filesystem, downloading it from
        data.world first, if necessary.

        This function returns an object of type `LocalDataset`. The object
        allows access to metedata via it's `describe()` method and to all the
        data via three properties `raw_data`, `tables` and `dataframes`, all
        of which are mappings (dict-like structures).

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id or of a url
        force_update : bool
            Flag, indicating if a new copy of the dataset should be downloaded
            replacing any previously downloaded copy
        auto_update: bool
            Flag, indicating that dataset be updated to the latest version

        Returns
        -------
        LocalDataset
            The object representing the dataset

        Raises
        ------
        RestApiError
            If a server error occurs
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        cache_dir = path.join(self._config.cache_dir, owner_id, dataset_id,
                              'latest')
        backup_dir = None
        if path.isdir(cache_dir) and force_update:
            backup_dir = path.join(self._config.cache_dir, owner_id,
                                   dataset_id, 'backup')
            move_cache_dir_to_backup_dir(backup_dir, cache_dir)

        descriptor_file = path.join(cache_dir, 'datapackage.json')
        if not path.isfile(descriptor_file):
            try:
                descriptor_file = self.api_client.download_datapackage(
                    dataset_key, cache_dir)
            except RestApiError as e:
                if backup_dir is not None:
                    shutil.move(backup_dir, cache_dir)
                    warn('Unable to download datapackage ({}). '
                         'Loading previously saved version.'.format(e.reason))
                else:
                    raise
        else:
            try:
                dataset_info = self.api_client.get_dataset(dataset_key)
            except RestApiError as e:
                return LocalDataset(descriptor_file)

            last_modified = datetime.strptime(dataset_info['updated'],
                                              '%Y-%m-%dT%H:%M:%S.%fZ')
            if (last_modified > datetime.utcfromtimestamp(
                    path.getmtime(str(descriptor_file)))):
                if auto_update:
                    try:
                        backup_dir = path.join(self._config.cache_dir,
                                                owner_id,dataset_id,
                                                'backup')
                        move_cache_dir_to_backup_dir(backup_dir,
                                                     cache_dir)
                        descriptor_file = self.api_client.download_datapackage(dataset_key, cache_dir)
                    except RestApiError as e:
                        if backup_dir is not None:
                            shutil.move(backup_dir, cache_dir)
                            warn('Unable to auto update datapackage ({}). '
                                 'Loading previously saved version.'.format(e.reason))
                        else:
                            raise
                else:
                    filterwarnings('always',
                        message='You are using an outdated copy')
                    warn('You are using an outdated copy of {}. '
                        'If you wish to use the latest version, call this '
                        'function with the argument '
                        'auto_update=True or '
                        'force_update=True'.format(dataset_key))

        if backup_dir is not None:
            shutil.rmtree(backup_dir, ignore_errors=True)

        return LocalDataset(descriptor_file)

    def open_remote_file(self, dataset_key, file_name,
                         mode='w', **kwargs):
        """
        Open a remote file object that can be used to write to or read from
        a file in a data.world dataset

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        file_name: str
            The name of the file to open
        mode: str, optional
            the mode for the file - must be 'w', 'wb', 'r', or 'rb' -
            indicating read/write ('r'/'w') and optionally "binary"
            handling of the file data.
        chunk_size: int, optional
            size of chunked bytes to return when reading streamed bytes
            in 'rb' mode
        decode_unicode: bool, optional
            whether to decode textual responses as unicode when returning
            streamed lines in 'r' mode

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
        try:
            return RemoteFile(self._config, dataset_key, file_name,
                              mode=mode, **kwargs)
        except Exception as e:
            raise RestApiError(cause=e)


class UriParam():
    """
    Represents a URI value as a parameter to a SPARQL query
    """
    def __init__(self, uri):
        """
        Initialize the UriParam value
        :param uri: the uri value to wrap
        """
        self._uri = uri

    def __repr__(self):
        """
        The official string representation for the URI
        :return: the string representation for the URI
        """
        return self._uri


# convert a literal into the SPARQL format expected by the REST endpoint
def convert_to_sparql_literal(value):
    if isinstance(value, bool):
        return "\"{}\"^^<http://www.w3.org/2001/XMLSchema#boolean>".format(
            str(value).lower())
    elif isinstance(value, numbers.Integral):
        return "\"{}\"^^<http://www.w3.org/2001/XMLSchema#integer>".format(
            value)
    elif isinstance(value, numbers.Number):
        return "\"{}\"^^<http://www.w3.org/2001/XMLSchema#decimal>".format(
            value)
    elif isinstance(value, UriParam):
        return "<{}>".format(repr(value))
    else:
        return "\"{}\"".format(value)


# move cache directory into backup directory
def move_cache_dir_to_backup_dir(backup_dir, cache_dir):
    if path.isdir(backup_dir):
        shutil.rmtree(backup_dir)
    shutil.move(cache_dir, backup_dir)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
