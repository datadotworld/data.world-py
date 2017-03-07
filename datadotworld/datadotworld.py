"""
data.world-py
Copyright 2017 data.world, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the
License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.

This product includes software developed at data.world, Inc.(http://www.data.world/).
"""
from __future__ import absolute_import

import requests

from .client.api import ApiClient
from .config import Config
from .models.query import Results


class DataDotWorld:
    def __init__(self, profile='default', **kwargs):
        config = Config(profile)

        self._token = config.auth_token

        # Overrides, for testing
        self._protocol = kwargs.get('protocol', 'https')
        self._query_host = kwargs.get('query_host', 'query.data.world')

        self.api_client = ApiClient(profile)

    def query(self, dataset_key, query, query_type="sql"):
        """Query an existing dataset

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
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

        Examples
        --------
        >>> results = dw.query('jonloyens/an-intro-to-dataworld-dataset',
        >>>                    'SELECT * FROM `DataDotWorldBBallStats`, `DataDotWorldBBallTeam` '
        >>>                    'WHERE DataDotWorldBBallTeam.Name = DataDotWorldBBallStats.Name')
        >>> df = results.as_dataframe()
        >>> df.info()
        <class 'pandas.core.frame.DataFrame'>
        RangeIndex: 8 entries, 0 to 7
        Data columns (total 6 columns):
        Name              8 non-null object
        PointsPerGame     8 non-null float64
        AssistsPerGame    8 non-null float64
        Name.1            8 non-null object
        Height            8 non-null object
        Handedness        8 non-null object
        dtypes: float64(2), object(4)
        memory usage: 456.0+ bytes
        """
        from . import __version__
        params = {
            "query": query
        }
        url = "{0}://{1}/{2}/{3}".format(self._protocol,
                                         self._query_host,
                                         query_type,
                                         dataset_key)
        headers = {
            'User-Agent': 'data.world-py - {0}'.format(__version__),
            'Accept': 'text/csv',
            'Authorization': 'Bearer {0}'.format(self.token)
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return Results(response.text)
        raise RuntimeError('Error executing query: {}'.format(response.text))
