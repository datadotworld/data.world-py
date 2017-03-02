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
import os
import re

import requests
from datadotworld._rest import ApiClient
from datadotworld._rest import DatasetsApi
from datadotworld._rest import UploadsApi

from datadotworld.models import (DatasetCreateRequest, DatasetPatchRequest, DatasetPutRequest,
                                       DatasetSummaryResponse, SuccessMessage, FileBatchUpdateRequest,
                                       FileCreateOrUpdateRequest, FileSourceCreateOrUpdateRequest, Results)


class DataDotWorld:
    """A Python Client for Accessing data.world"""

    def __init__(self, token=None, props_file="~/.data.world",
                 protocol="https",
                 query_host="query.data.world", api_host="api.data.world"):

        regex = re.compile(r"^token\s*=\s*(\S.*)$")
        filename = os.path.expanduser(props_file)
        self.token = token
        if self.token is None and os.path.isfile(filename):
            with open(filename, 'r') as props:
                self.token = next(iter([regex.match(line.strip()).group(1) for line in props if regex.match(line)]),
                                  None)
        if self.token is None:
            raise RuntimeError((
                'you must either provide an API token to this constructor, or create a '
                '.data.world file in your home directory with your API token'))

        self.protocol = protocol
        self.query_host = query_host

        self._api_client = ApiClient(host="{}://{}/v0".format(protocol, api_host), header_name='Authorization',
                                     header_value='Bearer {}'.format(token))
        self._datasets_api = DatasetsApi(self._api_client)
        self._uploads_api = UploadsApi(self._api_client)

        self._dataset_key_pattern = re.compile('[a-z0-9-]+/[a-z0-9-]+')  # Not the most comprehensive, for simplicity

    # Dataset Operations

    def get_dataset(self, dataset_key):
        """Retrieve an existing dataset

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id

        Returns
        -------
        DatasetSummaryResponse
            The dataset object

        Raises
        ------
        ApiException
            If a server error occurs

        Examples
        --------
        >>> intro_dataset = dw.get_dataset('jonloyens/an-intro-to-dataworld-dataset')
        >>> print(intro_dataset.description)
        A dataset that serves as a quick introduction to data.world and some of our capabilities.  Follow along in \
        the summary!
        """
        return self._datasets_api.get_dataset(*(self._split_dataset_key(dataset_key)))

    def create_dataset(self, owner_id, dataset):
        """Create a new dataset

        Parameters
        ----------
        owner_id : str
            Username of the owner of the new dataset
        dataset : DatasetCreateRequest
            The new dataset object

        Returns
        -------
        SuccessMessage
            Short message indicating success of the operation

        Raises
        ------
        ApiException
            If a server error occurs

        Examples
        --------
        >>> intro_dataset = DatasetCreateRequest()
        >>> intro_dataset.title = 'An intro to data.world dataset'
        >>> intro_dataset.visibility = 'OPEN'
        >>> intro_dataset.license = 'Public Domain License'
        >>> dw.create_dataset('jonloyens', intro_dataset)
        {'message': 'Dataset created successfully.'}
        """
        return self._datasets_api.create_dataset(owner_id, dataset)

    def patch_dataset(self, dataset_key, dataset):
        """Update an existing dataset

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        dataset : DatasetPatchRequest
            The dataset patch object, with only the attributes that need to change

        Returns
        -------
        SuccessMessage
            Short message indicating success of the operation

        Raises
        ------
        ApiException
            If a server error occurs

        Examples
        --------
        >>> intro_dataset_patch = DatasetPatchRequest()
        >>> intro_dataset_patch.tags = ['demo', 'datadotworld']
        >>> dw.patch_dataset('jonloyens/an-intro-to-dataworld-dataset', intro_dataset_patch)
        {'message': 'Dataset updated successfully.'}
        """
        owner_id, dataset_id = self._split_dataset_key(dataset_key)
        return self._datasets_api.patch_dataset(owner_id, dataset_id, dataset)

    def replace_dataset(self, dataset_key, dataset):
        """Replace an existing dataset

        *This method will completely overwrite an existing dataset.*

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        dataset : DatasetPutRequest
            The dataset object, redefining the entire dataset

        Returns
        -------
        SuccessMessage
            Short message indicating success of the operation

        Raises
        ------
        ApiException
            If a server error occurs

        Examples
        --------
        >>> intro_dataset_overwrite = DatasetPutRequest(
        >>>     description='A dataset that serves as a quick introduction to data.world',
        >>>     tags=['demo', 'datadotworld'],
        >>>     visibility='OPEN',
        >>>     license='Other')
        >>> dw.replace_dataset('jonloyens/an-intro-to-dataworld-dataset', intro_dataset_overwrite)
        {'message': 'Dataset replaced successfully.'}
        """
        owner_id, dataset_id = self._split_dataset_key(dataset_key)
        return self._datasets_api.replace_dataset(owner_id, dataset_id, dataset)

    # File Operations

    def add_files_via_url(self, dataset_key,
                          files):
        """Add or update dataset files linked to source URLs

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        files : list of FileCreateOrUpdateRequest
            The list of files to be added to the dataset or updated with a new URL

        Returns
        -------
        SuccessMessage
            Short message indicating success of the operation

        Raises
        ------
        ApiException
            If a server error occurs

        Examples
        --------
        >>> atx_basketball = FileCreateOrUpdateRequest(
        >>>     name='atx_startup_league_ranking.csv',
        >>>     source=FileSourceCreateOrUpdateRequest(
        >>>         url='http://www.atxsa.com/sports/basketball/startup_league_ranking.csv'))
        >>> dw.add_files_via_url('jonloyens/an-intro-to-dataworld-dataset',
        >>>                      FileBatchUpdateRequest(files=[atx_basketball]))
        {'message': 'Dataset successfully updated with new sources. Sync in progress.'}
        """
        owner_id, dataset_id = self._split_dataset_key(dataset_key)
        return self._datasets_api.add_files_by_source(owner_id, dataset_id, files)

    def sync_files(self, dataset_key):
        """Trigger synchronization process to update all dataset files linked to source URLs

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id

        Returns
        -------
        SuccessMessage
            Short message indicating success of the operation

        Raises
        ------
        ApiException
            If a server error occurs

        Examples
        --------
        >>> dw.sync_files('jonloyens/an-intro-to-dataworld-dataset')
        {'message': 'Sync started.'}
        """
        return self._datasets_api.sync(*(self._split_dataset_key(dataset_key)))

    def upload_files(self, dataset_key, files):
        """Upload dataset files

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        files : list of str
            The list of names/paths for files stored in the local filesystem

        Returns
        -------
        SuccessMessage
            Short message indicating success of the operation

        Raises
        ------
        ApiException
            If a server error occurs

        Examples
        --------
        >>> dw.upload_files('jonloyens/an-intro-to-dataworld-dataset',
        >>>                 ['/Users/jon/DataDotWorldBBall/DataDotWorldBBallTeam.csv'])
        {'message': 'File(s) uploaded.'}
        """
        owner_id, dataset_id = self._split_dataset_key(dataset_key)
        return self._uploads_api.upload_files(owner_id, dataset_id, files)

    def delete_files(self, dataset_key, names):
        """Delete dataset file(s)

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        names : list of str
            The list of names for files to be deleted

        Returns
        -------
        SuccessMessage
            Short message indicating success of the operation

        Raises
        ------
        ApiException
            If a server error occurs

        Examples
        --------
        >>> dw.delete_files('jonloyens/an-intro-to-dataworld-dataset', ['atx_startup_league_ranking.csv'])
        {'message': 'Dataset file(s) have been successfully deleted.'}
        """
        owner_id, dataset_id = self._split_dataset_key(dataset_key)
        return self._datasets_api.delete_files_and_sync_sources(owner_id, dataset_id, names)

    # Query Operations

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
        url = "{0}://{1}/{2}/{3}".format(self.protocol,
                                         self.query_host,
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
        raise RuntimeError('error running query.')

    def _split_dataset_key(self, dataset_key):
        if not re.match(self._dataset_key_pattern, dataset_key):
            raise ValueError('Invalid dataset key. Key must include user and dataset names, separated by / '
                             '(i.e. user/dataset).')
        owner_id, dataset_id = dataset_key.split('/')
        return owner_id, dataset_id
