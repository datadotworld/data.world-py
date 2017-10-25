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

from __future__ import absolute_import, division

import glob
import json
import os
import shutil
import uuid
import zipfile
from os import path

import requests

from datadotworld.client import _swagger
from datadotworld.util import parse_dataset_key, _user_agent


class RestApiClient(object):
    """REST API client

    Parameters
    ----------
    profile : str, optional
        Name of the configuration profile to use
    """

    def __init__(self, config):
        self._config = config
        self._protocol = 'https'
        self._download_host = 'download.data.world'

        api_host = 'api.data.world'
        self._host = "{}://{}/v0".format(self._protocol, api_host)
        swagger_client = _swagger.ApiClient(
            host=self._host,
            header_name='Authorization',
            header_value='Bearer {}'.format(self._config.auth_token))
        swagger_client.user_agent = _user_agent()

        self._datasets_api = _swagger.DatasetsApi(swagger_client)
        self._uploads_api = _swagger.UploadsApi(swagger_client)
        self._user_api = _swagger.UserApi(swagger_client)
        self._sql_api = _swagger.SqlApi(swagger_client)
        self._sparql_api = _swagger.SparqlApi(swagger_client)
        self._download_api = _swagger.DownloadApi(swagger_client)

    # Dataset Operations

    def get_dataset(self, dataset_key):
        """Retrieve an existing dataset definition

        This method retrieves metadata about an existing

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id

        Returns
        -------
        dict
            Dataset definition, with all attributes

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> intro_dataset = api_client.get_dataset(
        ...     'jonloyens/an-intro-to-dataworld-dataset')
        >>> intro_dataset['title']
        'An Intro to data.world Dataset'
        """
        try:
            return self._datasets_api.get_dataset(
                *(parse_dataset_key(dataset_key))).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def create_dataset(self, owner_id, **kwargs):
        """Create a new dataset

        Parameters
        ----------
        owner_id : str
            Username of the owner of the new dataset
        title : str
            Dataset title (will be used to generate dataset id on creation)
        description : str, optional
            Dataset description
        summary : str, optional
            Dataset summary markdown
        tags : list, optional
            Dataset tags
        license : {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY',
                   'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 'CC BY-NC-SA', 'Other'}
            Dataset license
        visibility : {'OPEN', 'PRIVATE'}
            Dataset visibility
        files : dict, optional
            File names and source URLs

        Returns
        -------
        str
            Newly created dataset key

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.create_dataset(
        ...     'username', title='Test dataset', visibility='PRIVATE',
        ...     license='Public Domain')  # doctest: +SKIP
        """
        request = self.__build_dataset_obj(
            lambda: _swagger.DatasetCreateRequest(),
            lambda name, url, description, labels : _swagger.FileCreateRequest(
                name=name,
                source=_swagger.FileSourceCreateRequest(url=url),
                description=description,
                labels=labels),
            kwargs)
        try:
            (_, _, headers) = self._datasets_api.create_dataset_with_http_info(
                owner_id, request, _return_http_data_only=False)
            if 'Location' in headers:
                return headers['Location']
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def update_dataset(self, dataset_key, **kwargs):
        """Update an existing dataset

        Parameters
        ----------
        title: str, optional
            Dataset title
        description : str, optional
            Dataset description
        summary : str, optional
            Dataset summary markdown
        tags : list, optional
            Dataset tags
        license : {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY',
                   'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 'CC BY-NC-SA', 'Other'}
            Dataset license
        visibility : {'OPEN', 'PRIVATE'}, optional
            Dataset visibility
        files : dict, optional
            File names and source URLs to add or update

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.update_dataset(
        ...    'username/test-dataset',
        ...    tags=['demo', 'datadotworld'])  # doctest: +SKIP
        """
        request = self.__build_dataset_obj(
            lambda: _swagger.DatasetPatchRequest(),
            lambda name, url, description, labels: _swagger.FileCreateOrUpdateRequest(
                name=name,
                source=_swagger.FileSourceCreateOrUpdateRequest(url=url),
                description=description,
                labels=labels),
            kwargs)

        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.patch_dataset(owner_id, dataset_id, request)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def replace_dataset(self, dataset_key, **kwargs):
        """Replace an existing dataset

        *This method will completely overwrite an existing dataset.*

        Parameters
        ----------
        title: str, optional
            Dataset title
        description : str, optional
            Dataset description
        summary : str, optional
            Dataset summary markdown
        tags : list, optional
            Dataset tags
        license : {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY',
                   'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 'CC BY-NC-SA', 'Other'}
            Dataset license
        visibility : {'OPEN', 'PRIVATE'}
            Dataset visibility
        files : dict, optional
            File names and source URLs to add or update

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.replace_dataset(
        ...    'username/test-dataset',
        ...    visibility='PRIVATE', license='Public Domain',
        ...    description='A better description')  # doctest: +SKIP
        """
        request = self.__build_dataset_obj(
            lambda: _swagger.DatasetPutRequest(),
            lambda name, url, description, labels: _swagger.FileCreateRequest(
                name=name,
                source=_swagger.FileSourceCreateRequest(url=url),
                description=description,
                labels=labels),
            kwargs)

        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.replace_dataset(owner_id, dataset_id, request)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def delete_dataset(self, dataset_key):
        """Deletes a dataset and all associated data

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id

        Returns
        -------
        str
            Success message for deleted dataset

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.delete_dataset(
        ...     'jonloyens/an-intro-to-dataworld-dataset')
        >>> del_dataset.message
        'Dataset has been successfully deleted.'
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._datasets_api.delete_dataset(owner_id, dataset_id)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # File Operations

    def add_files_via_url(self, dataset_key, files={}, **kwargs):
        """Add or update dataset files linked to source URLs

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        files : dict
            File names, description, labels and source URLs to add or update

        *description and labels are both optional.*

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> url = 'http://www.acme.inc/example.csv'
        >>> api_client = dw.api_client()
        >>> api_client.add_files_via_url(
        ...    'username/test-dataset',
        ...    {'example.csv': url}, description='file description')  # doctest: +SKIP
        """

        file_requests = [_swagger.FileCreateOrUpdateRequest(
            name=name,
            source=_swagger.FileSourceCreateOrUpdateRequest(url=url),
            **kwargs) for name, url in files.items()]

        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.add_files_by_source(
                owner_id, dataset_id,
                _swagger.FileBatchUpdateRequest(files=file_requests))
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def sync_files(self, dataset_key):
        """
        Trigger synchronization process to update all dataset files linked to
        source URLs.

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.sync_files('username/test-dataset')  # doctest: +SKIP
        """
        try:
            self._datasets_api.sync(*(parse_dataset_key(dataset_key)))
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def upload_files(self, dataset_key, files, **kwargs):
        """Upload dataset files

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        files : list of str
            The list of names/paths for files stored in the local filesystem
        expand_archives: bool optional
            Boolean value to indicate files should be expanded upon upload

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.upload_files(
        ...     'username/test-dataset',
        ...     ['/my/local/example.csv'])  # doctest: +SKIP
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._uploads_api.upload_files(owner_id, dataset_id, files, **kwargs)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def upload_file(self, dataset_key, name, **kwargs):
        """Upload one file to a dataset

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        name : str
            File name
        expand_archive: bool optional
            Boolean value to indicate files should be expanded upon upload

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.upload_file(
        ...     'username/test-dataset',
        ...     'example.csv')  # doctest: +SKIP
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._uploads_api.upload_file(owner_id, dataset_id, name, **kwargs)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def delete_files(self, dataset_key, names):
        """Delete dataset file(s)

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        names : list of str
            The list of names for files to be deleted

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.delete_files(
        ...     'username/test-dataset', ['example.csv'])  # doctest: +SKIP
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.delete_files_and_sync_sources(
                owner_id, dataset_id, names)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Datapackage

    def download_datapackage(self, dataset_key, dest_dir):
        """
        Download and unzip a dataset's datapackage

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        dest_dir : str or path
            Directory under which datapackage should be saved

        Returns
        -------
        path
            Location of the datapackage descriptor (datapackage.json) in the
            local filesystem

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> datapackage_descriptor = api_client.download_datapackage(
        ...     'jonloyens/an-intro-to-dataworld-dataset', '/tmp/test')
        >>> datapackage_descriptor
        '/tmp/test/datapackage.json'
        """
        if path.isdir(dest_dir):
            raise ValueError('dest_dir must be a new directory, '
                             'but {} already exists'.format(dest_dir))

        owner_id, dataset_id = parse_dataset_key(dataset_key)
        url = "{0}://{1}/datapackage/{2}/{3}".format(
            self._protocol, self._download_host, owner_id, dataset_id)
        headers = {
            'User-Agent': _user_agent(),
            'Authorization': 'Bearer {0}'.format(self._config.auth_token)
        }

        try:
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RestApiError(cause=e)

        unzip_dir = path.join(self._config.tmp_dir, str(uuid.uuid4()))
        os.makedirs(unzip_dir)

        zip_file = path.join(unzip_dir, 'dataset.zip')

        with open(zip_file, 'wb') as f:
            for data in response.iter_content(chunk_size=4096):
                f.write(data)

        zip_obj = zipfile.ZipFile(zip_file)
        zip_obj.extractall(path=unzip_dir)

        # Find where datapackage.json is within expanded files
        unzipped_descriptor = glob.glob(
            '{}/**/datapackage.json'.format(unzip_dir))
        if not unzipped_descriptor:
            raise RuntimeError(
                'Zip file did not contain a datapackage manifest.')

        unzipped_dir = path.dirname(unzipped_descriptor[0])

        shutil.move(unzipped_dir, dest_dir)
        shutil.rmtree(unzip_dir, ignore_errors=True)

        return path.join(dest_dir, 'datapackage.json')

    # User Operations

    def get_user_data(self):
        """Retrieve data for authenticated user

        Parameters
        ----------
        no parameters

        Returns
        -------
        dict
            User data, with all attributes

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_data = api_client.get_user_data()
        >>> user_data.displayName
        'Name User'
        """
        try:
            return self._user_api.get_user_data()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def fetch_contributing_datasets(self):
        """Fetch datasets that the authenticated user has access to

        Parameters
        ----------
        limit : str, optional
            Maximum number of items to include in a page of results
        next : str, optional
            Token from previous result page (to be used when requesting a subsequent page)
        sort : str, optional
            Property name to sort

        Returns
        -------
        dict
            Authenticated user dataset

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_dataset = api_client.fetch_contributing_datasets()
        {'count': 0, 'records': [], 'next_page_token': None}
        """
        try:
            return self._user_api.fetch_contributing_datasets()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def fetch_liked_datasets(self):
        """Fetch datasets that authenticated user likes

        Parameters
        ----------
        limit : str, optional
            Maximum number of items to include in a page of results
        next : str, optional
            Token from previous result page (to be used when requesting a subsequent page)
        sort : str, optional
            Property name to sort

        Returns
        -------
        dict
            Dataset definition, with all attributes

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_liked_dataset = api_client.fetch_liked_datasets()
        >>> user_liked_dataset.count
        1
        """
        try:
            return self._user_api.fetch_liked_datasets()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def fetch_datasets(self):
        """Fetch authenticated user owned datasets

        Parameters
        ----------
        limit : str, optional
            Maximum number of items to include in a page of results
        next : str, optional
            Token from previous result page (to be used when requesting a subsequent page)
        sort : str, optional
            Property name to sort

        Returns
        -------
        dict
            Dataset definition, with all attributes

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_owned_dataset = api_client.fetch_datasets()
        >>> user_owned_dataset.records
        []
        """
        try:
            return self._user_api.fetch_datasets()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Sql Operations

    def sql_get(self, dataset_key, query):
        """Executes SQL queries against a dataset via GET

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        query : str
            SQL query
        include_table_schema : bool
            Flags indicating to include table schema in the response

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> query = 'SELECT * FROM test-dataset'
        >>> api_client.sql_get('username/test-dataset', query)
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._sql_api.sql_get(owner_id, dataset_id, query)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def sql_post(self, dataset_key, query):
        """Executes SQL queries against a dataset via POST

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        query : str
            SQL query
        include_table_schema : bool
            Flags indicating to include table schema in the response

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.sql_post('username/test-dataset', query)
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._sql_api.sql_post(owner_id, dataset_id, query)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Sparql Operations

    def sparql_get(self, dataset_key, query):
        """Executes SPARQL queries against a dataset via GET

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        query : str
            SPARQL query

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.sparql_get('username/test-dataset', query)
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._sparql_api.sparql_get(owner_id, dataset_id, query)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def sparql_post(self, dataset_key, query):
        """Executes SPARQL queries against a dataset via POST

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        query : str
            SPARQL query

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.sparql_post('username/test-dataset', query)
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._sparql_api.sparql_post(owner_id, dataset_id, query)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Download Operations

    def download_dataset(self, dataset_key):
        """Return a .zip containing all files within the dataset as uploaded.

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.download_dataset('username/test-dataset')
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._download_api.download_dataset(owner_id, dataset_id)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def download_file(self, dataset_key, file):
        """Return a .zip of a files within the dataset as uploaded.

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id

        file : str
            File path to be returned

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.download_file('username/test-dataset', ['/my/local/example.csv'])
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._download_api.download_file(owner_id, dataset_id, file)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    @staticmethod
    def __build_dataset_obj(dataset_constructor, file_constructor, args):
        files = ([file_constructor(name, url)
                  for name, url in args['files'].items()]
                 if 'files' in args else None)

        dataset = dataset_constructor()
        if 'title' in args:
            dataset.title = args['title']
        if 'description' in args:
            dataset.description = args['description']
        if 'summary' in args:
            dataset.summary = args['summary']
        if 'tags' in args:
            dataset.tags = args['tags']
        if 'license' in args:
            dataset.license = args.get('license')
        if 'visibility' in args:
            dataset.visibility = args['visibility']

        dataset.files = files

        return dataset


class RestApiError(Exception):
    """
    Exception wrapper for errors raised by requests or by the swagger client
    """

    def __init__(self, *args, **kwargs):
        self.cause = kwargs.pop('cause', None)
        self.status, self.reason, self.body = None, None, None
        if self.cause is not None:
            if type(self.cause) is _swagger.rest.ApiException:
                self.status = self.cause.status
                self.reason = self.cause.reason
                self.body = self.cause.body
            elif type(self.cause) is requests.RequestException:
                requests_response = self.cause.response
                if requests_response is not None:
                    self.status = requests_response.status_code
                    self.reason = requests_response.reason
                    self.body = requests_response.content
                    self.json = requests_response.json  # Delegates to requests

        self.status = kwargs.pop('status', self.status)
        self.reason = kwargs.pop('reason', self.reason)
        self.body = kwargs.pop('body', self.body)
        super(RestApiError, self).__init__(*args, **kwargs)

    def json(self):
        """Attempts to parse json in the body of response to failed requests

        Data.world often includes a JSON body for errors; however, there are no
        guarantees.

        Returns
        -------
        json
            The JSON body if one is included. Otherwise, None.
        """
        try:
            return json.loads(self.body)
        except (ValueError, TypeError):
            return None

    def __str__(self):
        return str(self.json() or self.cause)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
