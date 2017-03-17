"""
data.world-py
Copyright 2017 data.world, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the
License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.

This product includes software developed at
data.world, Inc.(http://data.world/).
"""
from __future__ import absolute_import

import shutil
import weakref
from os import path
from warnings import warn

import requests

from datadotworld.client.api import RestApiClient, RestApiError
from datadotworld.config import Config
from datadotworld.models.dataset import LocalDataset
from datadotworld.models.query import QueryResults
from datadotworld.util import _user_agent, parse_dataset_key


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

    def __init__(self, profile='default', **kwargs):
        # Overrides, for testing
        self._config = kwargs.get('config', Config(profile))

        self._protocol = 'https'
        self._query_host = 'query.data.world'
        self._download_host = 'download.data.world'
        self.api_client = RestApiClient(self._config)

    def query(self, dataset_key, query, query_type="sql"):
        """Query an existing dataset

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id or of a url
        query : str
            SQL or SPARQL query
        query_type : {'sql', 'sparql'}, optional
            The type of the query. Must be either 'sql' or 'sparql'.

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
        url = "{0}://{1}/{2}/{3}/{4}".format(self._protocol, self._query_host,
                                             query_type, owner_id, dataset_id)
        headers = {
            'User-Agent': _user_agent(),
            'Accept': 'text/csv',
            'Authorization': 'Bearer {0}'.format(self._config.auth_token)
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return QueryResults(response.text)
        raise RuntimeError('Error executing query: {}'.format(response.text))

    def load_dataset(self, dataset_key, force_update=False):
        """
        Load a dataset from the local filesystem, downloading it from
        data.world first, if necessary

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id or of a url
        force_update : bool
            Flag, indicating if a new copy of the dataset should be downloaded
            replacing any previously downloaded copy

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
            if path.isdir(backup_dir):
                shutil.rmtree(backup_dir)
            shutil.move(cache_dir, backup_dir)

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

        if backup_dir is not None:
            shutil.rmtree(backup_dir, ignore_errors=True)

        return LocalDataset(descriptor_file)


# Convenience top-level functions

__instances = weakref.WeakValueDictionary()


def _get_instance(profile):
    instance = __instances.get(profile)
    if instance is None:
        instance = DataDotWorld(profile=profile)
        __instances[profile] = instance
    return instance


def load_dataset(dataset_key, force_update=False, profile='default'):
    """
    Load a dataset from the local filesystem, downloading it from data.world
    first, if necessary

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


def query(dataset_key, query, query_type='sql', profile='default'):
    """Query an existing dataset

    Parameters
    ----------
    dataset_key : str
        Dataset identifier, in the form of owner/id or of a url
    query : str
        SQL or SPARQL query
    query_type : {'sql', 'sparql'}, optional
        The type of the query. Must be either 'sql' or 'sparql'.
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
                                        query_type=query_type)


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
