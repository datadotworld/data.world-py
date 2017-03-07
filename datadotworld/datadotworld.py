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

import os
import shutil
import uuid
import zipfile
from os.path import join, isdir
from warnings import warn

import progressbar
import requests

from datadotworld.client.api import RestApiClient
from datadotworld.config import Config
from datadotworld.models.dataset import LocalDataset
from datadotworld.models.query import Results
from datadotworld.util import user_agent


class DataDotWorld:
    def __init__(self, profile='default', **kwargs):
        self._config = Config(profile)

        # Overrides, for testing
        self._protocol = kwargs.get('protocol', 'https')
        self._query_host = kwargs.get('query_host', 'query.data.world')
        self._download_host = kwargs.get('download_host', 'download.data.world')

        self.api_client = RestApiClient(profile)

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
        memory usage: 456.0bytes
        """
        params = {
            "query": query
        }
        url = "{0}://{1}/{2}/{3}".format(self._protocol,
                                         self._query_host,
                                         query_type,
                                         dataset_key)
        headers = {
            'User-Agent': user_agent(),
            'Accept': 'text/csv',
            'Authorization': 'Bearer {0}'.format(self._config.auth_token)
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return Results(response.text)
        raise RuntimeError('Error executing query: {}'.format(response.text))

    def load_dataset(self, dataset_key):

        url = "{0}://{1}/datapackage/{2}".format(self._protocol, self._download_host, dataset_key)
        headers = {
            'User-Agent': user_agent(),
            'Authorization': 'Bearer {0}'.format(self._config.auth_token)
        }

        data_dir = join(self._config.cache_dir, dataset_key, 'latest')
        descriptor_file = join(data_dir, 'datapackage.json')

        try:
            response = requests.get(url, headers=headers, stream=True)
        except requests.RequestException as e:
            if os.path.exists(descriptor_file):
                warn('Unable to download datapackage for {}. Loaded from cache at {}'.format(
                    dataset_key, data_dir))
                return LocalDataset(descriptor_file)
            else:
                raise e

        if response.status_code == 200:
            unzip_dir = join(self._config.tmp_dir, str(uuid.uuid4()))
            os.makedirs(unzip_dir)

            zip_file = join(unzip_dir, 'dataset.zip')
            content_length = len(response.content) if response.content is not None else progressbar.UnknownLength

            with progressbar.ProgressBar(max_value=content_length) as bar, \
                    open(zip_file, 'wb') as f:

                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    if bar.max_value == progressbar.UnknownLength or (bar.max_value - bar.value) > 4096:
                        bar.update(bar.value + 4096)
                    else:
                        bar.update(bar.max_value)

            z = zipfile.ZipFile(zip_file)  # extract to tmp
            z.extractall(path=unzip_dir)
            unzipped_dir = [join(unzip_dir, dir) for dir in os.listdir(unzip_dir) if isdir(join(unzip_dir, dir))][0]

            # TODO: Calculate overwrite based on dataset last modified
            overwrite = True
            if os.path.exists(data_dir):
                if overwrite:
                    shutil.rmtree(data_dir)
                shutil.move(unzipped_dir, data_dir)
            else:
                shutil.move(unzipped_dir, data_dir)

            shutil.rmtree(unzip_dir, ignore_errors=True)

            return LocalDataset(descriptor_file)

        else:
            if os.path.exists(descriptor_file):
                warn('Unable to download datapackage for {} (HTTP error: {}). Loaded from cache at {}'.format(
                    dataset_key, response.status_code, data_dir))
                return LocalDataset(descriptor_file)
            else:
                raise RuntimeError(
                    'Unable to download datapackage for {} (HTTP error: {})'.format(dataset_key, response.status_code))
