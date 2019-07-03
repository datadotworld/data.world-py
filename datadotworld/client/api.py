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

import functools
import glob
import json
import os
import shutil
import uuid
import zipfile
from os import path

import requests
import six

from datadotworld.client import _swagger
from datadotworld.client.content_negotiating_api_client import (
    ContentNegotiatingApiClient
)
from datadotworld.util import parse_dataset_key, _user_agent
from datadotworld.hosts import API_HOST, DOWNLOAD_HOST


class RestApiClient(object):
    """REST API client

    :param profile: Name of the configuration profile to use
    :type profile: str optional
    """

    def __init__(self, config):
        self._config = config

        self._host = "{}/v0".format(API_HOST)
        swagger_client = _swagger.ApiClient(
            host=self._host,
            header_name='Authorization',
            header_value='Bearer {}'.format(self._config.auth_token))
        swagger_client.user_agent = _user_agent()

        self._build_api_client = functools.partial(
            ContentNegotiatingApiClient,
            host=self._host,
            header_name='Authorization',
            header_value='Bearer {}'.format(self._config.auth_token),
            user_agent=_user_agent())

        self._datasets_api = _swagger.DatasetsApi(swagger_client)
        self._uploads_api = _swagger.UploadsApi(swagger_client)
        self._user_api = _swagger.UserApi(swagger_client)
        self._download_api = _swagger.DownloadApi(swagger_client)
        self._streams_api = _swagger.StreamsApi(swagger_client)
        self._projects_api = _swagger.ProjectsApi(swagger_client)
        self._insights_api = _swagger.InsightsApi(swagger_client)

    # Dataset Operations

    def get_dataset(self, dataset_key):
        """Retrieve an existing dataset definition

        This method retrieves metadata about an existing

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :returns: Dataset definition, with all attributes
        :rtype: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> intro_dataset = api_client.get_dataset(
        ...     'jonloyens/an-intro-to-dataworld-dataset')  # doctest: +SKIP
        >>> intro_dataset['title']  # doctest: +SKIP
        'An Intro to data.world Dataset'
        """
        try:
            return self._datasets_api.get_dataset(
                *(parse_dataset_key(dataset_key))).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def create_dataset(self, owner_id, **kwargs):
        """Create a new dataset

        :param owner_id: Username of the owner of the new dataset
        :type owner_id: str
        :param title: Dataset title (will be used to generate dataset id on
            creation)
        :type title: str
        :param description: Dataset description
        :type description: str, optional
        :param summary: Dataset summary markdown
        :type summary: str, optional
        :param tags: Dataset tags
        :type tags: list, optional
        :param license: Dataset license
        :type license: {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY',
            'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 'CC BY-NC-SA', 'Other'}
        :param visibility: Dataset visibility
        :type visibility: {'OPEN', 'PRIVATE'}
        :param files: File name as dict, source URLs, description and labels()
        as properties
        :type files: dict, optional
            *Description and labels are optional*
        :returns: Newly created dataset key
        :rtype: str
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> url = 'http://www.acme.inc/example.csv'
        >>> api_client.create_dataset(
        ...     'username', title='Test dataset', visibility='PRIVATE',
        ...     license='Public Domain',
        ...     files={'dataset.csv':{'url': url}})  # doctest: +SKIP
        """
        request = self.__build_dataset_obj(
            lambda: _swagger.DatasetCreateRequest(
                title=kwargs.get('title'),
                visibility=kwargs.get('visibility')),
            lambda name, url, expand_archive, description, labels:
            _swagger.FileCreateRequest(
                name=name,
                source=_swagger.FileSourceCreateRequest(
                    url=url,
                    expand_archive=expand_archive),
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

        :param description: Dataset description
        :type description: str, optional
        :param summary: Dataset summary markdown
        :type summary: str, optional
        :param tags: Dataset tags
        :type tags: list, optional
        :param license: Dataset license
        :type license: {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY',
            'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 'CC BY-NC-SA', 'Other'}
        :param visibility: Dataset visibility
        :type visibility: {'OPEN', 'PRIVATE'}, optional
        :param files: File names and source URLs to add or update
        :type files: dict, optional
        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :raises RestApiException: If a server error occurs

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
            lambda name, url, expand_archive, description, labels:
            _swagger.FileCreateOrUpdateRequest(
                name=name,
                source=_swagger.FileSourceCreateOrUpdateRequest(
                    url=url,
                    expand_archive=expand_archive)
                if url is not None else None,
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

        :param description: Dataset description
        :type description: str, optional
        :param summary: Dataset summary markdown
        :type summary: str, optional
        :param tags: Dataset tags
        :type tags: list, optional
        :param license: Dataset license
        :type license: {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY',
            'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 'CC BY-NC-SA', 'Other'}
        :param visibility: Dataset visibility
        :type visibility: {'OPEN', 'PRIVATE'}
        :param files: File names and source URLs to add or update
        :type files: dict, optional
        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :raises RestApiException: If a server error occurs

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
            lambda: _swagger.DatasetPutRequest(
                title=kwargs.get('title'),
                visibility=kwargs.get('visibility')
            ),
            lambda name, url, expand_archive, description, labels:
            _swagger.FileCreateRequest(
                name=name,
                source=_swagger.FileSourceCreateRequest(
                    url=url,
                    expand_archive=expand_archive),
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

        :params dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.delete_dataset(
        ...     'username/dataset')  # doctest: +SKIP
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.delete_dataset(owner_id, dataset_id)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # File Operations

    def add_files_via_url(self, dataset_key, files={}):
        """Add or update dataset files linked to source URLs

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :param files: Dict containing the name of files and metadata
            Uses file name as a dict containing File description, labels and
            source URLs to add or update (Default value = {})
            *description and labels are optional.*
        :type files: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> url = 'http://www.acme.inc/example.csv'
        >>> api_client = dw.api_client()
        >>> api_client.add_files_via_url(
        ...     'username/test-dataset',
        ...     {'example.csv': {
        ...         'url': url,
        ...         'labels': ['raw data'],
        ...         'description': 'file description'}})  # doctest: +SKIP
        """
        file_requests = [_swagger.FileCreateOrUpdateRequest(
            name=file_name,
            source=_swagger.FileSourceCreateOrUpdateRequest(
                url=file_info['url'],
                expand_archive=file_info.get('expand_archive',
                                             False)),
            description=file_info.get('description'),
            labels=file_info.get('labels'),
        ) for file_name, file_info in files.items()]
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.add_files_by_source(
                owner_id, dataset_id,
                _swagger.FileBatchUpdateRequest(files=file_requests))
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def sync_files(self, dataset_key):
        """Trigger synchronization process to update all dataset files linked to
        source URLs.

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :raises RestApiException: If a server error occurs

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

    def upload_files(self, dataset_key, files, files_metadata={}, **kwargs):
        """Upload dataset files

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :param files: The list of names/paths for files stored in the
        local filesystem
        :type files: list of str
        :param expand_archives: Boolean value to indicate files should be
        expanded upon upload
        :type expand_archive: bool optional
        :param files_metadata: Dict containing the name of files and metadata
            Uses file name as a dict containing File description, labels and
            source URLs to add or update
        :type files_metadata: dict optional
        :raises RestApiException: If a server error occurs

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
            self._uploads_api.upload_files(owner_id, dataset_id, files,
                                           **kwargs)
            if files_metadata:
                self.update_dataset(dataset_key, files=files_metadata)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def upload_file(self, dataset_key, name, file_metadata={}, **kwargs):
        """Upload one file to a dataset

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :param name: Name/path for files stored in the local filesystem
        :type name: str
        :param expand_archives: Boolean value to indicate files should be
        expanded upon upload
        :type expand_archive: bool optional
        :param files_metadata: Dict containing the name of files and metadata
        Uses file name as a dict containing File description, labels and
        source URLs to add or update
        :type files_metadata: dict optional
        :raises RestApiException: If a server error occurs

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
            if file_metadata:
                self.update_dataset(dataset_key, files=file_metadata)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def delete_files(self, dataset_key, names):
        """Delete dataset file(s)

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :param names: The list of names for files to be deleted
        :type names: list of str
        :raises RestApiException: If a server error occurs

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
        """Download and unzip a dataset's datapackage

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :param dest_dir: Directory under which datapackage should be saved
        :type dest_dir: str or path
        :returns: Location of the datapackage descriptor (datapackage.json) in
            the local filesystem
        :rtype: path
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> datapackage_descriptor = api_client.download_datapackage(
        ...     'jonloyens/an-intro-to-dataworld-dataset',
        ...     '/tmp/test')  # doctest: +SKIP
        >>> datapackage_descriptor  # doctest: +SKIP
        '/tmp/test/datapackage.json'
        """
        if path.isdir(dest_dir):
            raise ValueError('dest_dir must be a new directory, '
                             'but {} already exists'.format(dest_dir))

        owner_id, dataset_id = parse_dataset_key(dataset_key)
        url = "{0}/datapackage/{1}/{2}".format(
            DOWNLOAD_HOST, owner_id, dataset_id)
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

        :returns: User data, with all attributes
        :rtype: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_data = api_client.get_user_data()  # doctest: +SKIP
        >>> user_data[display_name]  # doctest: +SKIP
        'Name User'
        """
        try:
            return self._user_api.get_user_data().to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def fetch_contributing_datasets(self, **kwargs):
        """Fetch datasets that the authenticated user has access to

        :param limit: Maximum number of items to include in a page of results
        :type limit: str, optional
        :param next: Token from previous result page (to be used when
            requesting a subsequent page)
        :type next: str, optional
        :param sort: Property name to sort
        :type sort: str, optional
        :returns: Authenticated user dataset
        :rtype: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_dataset =
        ...     api_client.fetch_contributing_datasets()  # doctest: +SKIP
        {'count': 0, 'records': [], 'next_page_token': None}
        """
        try:
            return self._user_api.fetch_contributing_datasets(
                **kwargs).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def fetch_liked_datasets(self, **kwargs):
        """Fetch datasets that authenticated user likes

        :param limit: Maximum number of items to include in a page of results
        :type limit: str, optional
        :param next: Token from previous result page (to be used when
            requesting a subsequent page)
        :type next: str, optional
        :param sort: Property name to sort
        :type sort: str, optional
        :returns: Dataset definition, with all attributes
        :rtype: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_liked_dataset =
        ...     api_client.fetch_liked_datasets() # doctest: +SKIP
        """
        try:
            return self._user_api.fetch_liked_datasets(**kwargs).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def fetch_datasets(self, **kwargs):
        """Fetch authenticated user owned datasets

        :param limit: Maximum number of items to include in a page of results
        :type limit: str, optional
        :param next: Token from previous result page (to be used when
            requesting a subsequent page)
        :type next: str, optional
        :param sort: Property name to sort
        :type sort: str, optional
        :returns: Dataset definition, with all attributes
        :rtype: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_owned_dataset = api_client.fetch_datasets() # doctest: +SKIP
        """
        try:
            return self._user_api.fetch_datasets(**kwargs).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def fetch_contributing_projects(self, **kwargs):
        """Fetch projects that the currently authenticated user has access to

        :returns: Authenticated user projects
        :rtype: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_projects =
        ...     api_client.fetch_contributing_projects()  # doctest: +SKIP
        {'count': 0, 'records': [], 'next_page_token': None}
        """
        try:
            return self._user_api.fetch_contributing_projects(
                **kwargs).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def fetch_liked_projects(self, **kwargs):
        """Fetch projects that the currently authenticated user likes

        :returns: Authenticated user projects
        :rtype: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_liked_projects =
        ...     api_client.fetch_liked_projects() # doctest: +SKIP
        """
        try:
            return self._user_api.fetch_liked_projects(**kwargs).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def fetch_projects(self, **kwargs):
        """Fetch projects that the currently authenticated user owns

        :returns: Authenticated user projects
        :rtype: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> user_projects =
        ...     api_client.fetch_projects() # doctest: +SKIP
        """
        try:
            return self._user_api.fetch_projects(**kwargs).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Sql Operations

    def sql(self, dataset_key, query, desired_mimetype='application/json',
            **kwargs):
        """Executes SQL queries against a dataset via POST

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :param query: SQL query
        :type query: str
        :param include_table_schema: Flags indicating to include table schema
            in the response
        :type include_table_schema: bool
        :returns: file object that can be used in file parsers and
            data handling modules.
        :rtype: file-like object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.sql('username/test-dataset', 'query') # doctest: +SKIP
        """
        api_client = self._build_api_client(
            default_mimetype_header_accept=desired_mimetype)
        sql_api = kwargs.get('sql_api_mock', _swagger.SqlApi(api_client))
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            response = sql_api.sql_post(
                owner_id, dataset_id, query, _preload_content=False, **kwargs)
            return six.BytesIO(response.data)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Sparql Operations

    def sparql(self, dataset_key, query,
               desired_mimetype='application/sparql-results+json', **kwargs):
        """Executes SPARQL queries against a dataset via POST

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :param query: SPARQL query
        :type query: str
        :returns: file object that can be used in file parsers and
            data handling modules.
        :rtype: file object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.sparql_post('username/test-dataset',
        ...     query) # doctest: +SKIP
        """
        api_client = self._build_api_client(
            default_mimetype_header_accept=desired_mimetype)
        sparql_api = kwargs.get('sparql_api_mock',
                                _swagger.SparqlApi(api_client))
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            response = sparql_api.sparql_post(
                owner_id, dataset_id, query, _preload_content=False, **kwargs)
            return six.BytesIO(response.data)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Download Operations

    def download_dataset(self, dataset_key):
        """Return a .zip containing all files within the dataset as uploaded.

        :param dataset_key : Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :returns: .zip file contain files within dataset
        :rtype: file object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.download_dataset(
        ...     'username/test-dataset')  # doctest: +SKIP
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._download_api.download_dataset(owner_id, dataset_id)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def download_file(self, dataset_key, file):
        """Return a file within the dataset as uploaded.

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :param file: File path to be returned
        :type file: str
        :returns: file in which the data was uploaded
        :rtype: file object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.download_file('username/test-dataset',
        ...      '/my/local/example.csv')  # doctest: +SKIP
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._download_api.download_file(owner_id, dataset_id, file)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Streams Operation

    def append_records(self, dataset_key, stream_id, body):
        """Append records to a stream.

        :param dataset_key: Dataset identifier, in the form of owner/id
        :type dataset_key: str
        :param stream_id: Stream unique identifier.
        :type stream_id: str
        :param body: Object body
        :type body: obj
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.append_records('username/test-dataset','streamId',
        ...     {'content':'content'})  # doctest: +SKIP
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            return self._streams_api.append_records(owner_id, dataset_id,
                                                    stream_id, body)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Projects Operations

    def get_project(self, project_key):
        """Retrieve an existing project

        This method retrieves metadata about an existing project

        :param project_key: Project identifier, in the form of owner/id
        :type project_key: str
        :returns: Project definition, with all attributes
        :rtype: dict
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> intro_project = api_client.get_project(
        ...     'jonloyens/'
        ...     'an-example-project-that-shows-what-to-put-in-data-world'
        ... )  # doctest: +SKIP
        >>> intro_project['title']  # doctest: +SKIP
        'An Example Project that Shows What To Put in data.world'
        """
        try:
            owner_id, project_id = parse_dataset_key(project_key)
            return self._projects_api.get_project(owner_id,
                                                  project_id).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def create_project(self, owner_id, **kwargs):
        """Create a new project

        :param owner_id: Username of the creator of a
            project.
        :type owner_id: str
        :param title: Project title (will be used to generate project id on
            creation)
        :type title: str
        :param objective: Short project objective.
        :type objective: str, optional
        :param summary: Long-form project summary.
        :type summary: str, optional
        :param tags: Project tags. Letters numbers and spaces
        :type tags: list, optional
        :param license: Project license
        :type license: {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY',
            'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 'CC BY-NC-SA', 'Other'}
        :param visibility: Project visibility
        :type visibility: {'OPEN', 'PRIVATE'}
        :param files: File name as dict, source URLs, description and labels()
        as properties
        :type files: dict, optional
            *Description and labels are optional*
        :param linked_datasets: Initial set of linked datasets.
        :type linked_datasets: list of object, optional
        :returns: Newly created project key
        :rtype: str
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.create_project(
        ...     'username', title='project testing',
        ...     visibility='PRIVATE',
        ...     linked_datasets=[{'owner': 'someuser',
        ...                       'id': 'somedataset'}])  # doctest: +SKIP
        """
        request = self.__build_project_obj(
            lambda: _swagger.ProjectCreateRequest(
                title=kwargs.get('title'),
                visibility=kwargs.get('visibility')
            ),
            lambda name, url, description, labels:
            _swagger.FileCreateRequest(
                name=name,
                source=_swagger.FileSourceCreateRequest(url=url),
                description=description,
                labels=labels), kwargs)
        try:
            (_, _, headers) = self._projects_api.create_project_with_http_info(
                owner_id, body=request, _return_http_data_only=False)
            if 'Location' in headers:
                return headers['Location']
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def update_project(self, project_key, **kwargs):
        """Update an existing project

        :param project_key: Username and unique identifier of the creator of a
            project in the form of owner/id.
        :type project_key: str
        :param title: Project title
        :type title: str
        :param objective: Short project objective.
        :type objective: str, optional
        :param summary: Long-form project summary.
        :type summary: str, optional
        :param tags: Project tags. Letters numbers and spaces
        :type tags: list, optional
        :param license: Project license
        :type license: {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY',
            'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 'CC BY-NC-SA', 'Other'}
        :param visibility: Project visibility
        :type visibility: {'OPEN', 'PRIVATE'}
        :param files: File name as dict, source URLs, description and labels()
        as properties
        :type files: dict, optional
            *Description and labels are optional*
        :param linked_datasets: Initial set of linked datasets.
        :type linked_datasets: list of object, optional
        :returns: message object
        :rtype: object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.update_project(
        ...    'username/test-project',
        ...    tags=['demo', 'datadotworld'])  # doctest: +SKIP
        """
        request = self.__build_project_obj(
            lambda: _swagger.ProjectPatchRequest(),
            lambda name, url, description, labels:
            _swagger.FileCreateOrUpdateRequest(
                name=name,
                source=_swagger.FileSourceCreateOrUpdateRequest(url=url),
                description=description,
                labels=labels),
            kwargs)
        owner_id, project_id = parse_dataset_key(project_key)
        try:
            return self._projects_api.patch_project(owner_id,
                                                    project_id,
                                                    body=request)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def replace_project(self, project_key, **kwargs):
        """Replace an existing Project

        *Create a project with a given id or completely rewrite the project,
        including any previously added files or linked datasets, if one already
        exists with the given id.*

        :param project_key: Username and unique identifier of the creator of a
            project in the form of owner/id.
        :type project_key: str
        :param title: Project title
        :type title: str
        :param objective: Short project objective.
        :type objective: str, optional
        :param summary: Long-form project summary.
        :type summary: str, optional
        :param tags: Project tags. Letters numbers and spaces
        :type tags: list, optional
        :param license: Project license
        :type license: {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY',
            'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 'CC BY-NC-SA', 'Other'}
        :param visibility: Project visibility
        :type visibility: {'OPEN', 'PRIVATE'}
        :param files: File name as dict, source URLs, description and labels()
        as properties
        :type files: dict, optional
            *Description and labels are optional*
        :param linked_datasets: Initial set of linked datasets.
        :type linked_datasets: list of object, optional
        :returns: project object
        :rtype: object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.replace_project(
        ...    'username/test-project',
        ...    visibility='PRIVATE',
        ...    objective='A better objective',
        ...    title='Replace project')  # doctest: +SKIP
        """
        request = self.__build_project_obj(
            lambda: _swagger.ProjectCreateRequest(
                title=kwargs.get('title'),
                visibility=kwargs.get('visibility')
            ),
            lambda name, url, description, labels:
            _swagger.FileCreateRequest(
                name=name,
                source=_swagger.FileSourceCreateRequest(url=url),
                description=description,
                labels=labels),
            kwargs)
        try:
            project_owner_id, project_id = parse_dataset_key(project_key)
            self._projects_api.replace_project(project_owner_id,
                                               project_id,
                                               body=request)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def add_linked_dataset(self, project_key, dataset_key):
        """Link project to an existing dataset

        This method links a dataset to project

        :param project_key: Project identifier, in the form of owner/id
        :type project_key: str
        :param dataset_key: Dataset identifier, in the form of owner/id
        :type project_key: str
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> linked_dataset = api_client.add_linked_dataset(
        ...     'username/test-project',
        ...     'username/test-dataset')  # doctest: +SKIP
        """
        try:
            project_owner_id, project_id = parse_dataset_key(project_key)
            dataset_owner_id, dataset_id = parse_dataset_key(dataset_key)
            self._projects_api.add_linked_dataset(project_owner_id,
                                                  project_id,
                                                  dataset_owner_id,
                                                  dataset_id)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def remove_linked_dataset(self, project_key, dataset_key):
        """Unlink dataset

        This method unlinks a dataset from a project

        :param project_key: Project identifier, in the form of owner/id
        :type project_key: str
        :param dataset_key: Dataset identifier, in the form of owner/id
        :type project_key: str
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.remove_linked_dataset(
        ...    'username/test-project',
        ...    'username/test-dataset')  # doctest: +SKIP
        """
        try:
            project_owner_id, project_id = parse_dataset_key(project_key)
            dataset_owner_id, dataset_id = parse_dataset_key(dataset_key)
            self._projects_api.remove_linked_dataset(project_owner_id,
                                                     project_id,
                                                     dataset_owner_id,
                                                     dataset_id)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def delete_project(self, project_key):
        """Deletes a project and all associated data

        :params project_key: Project identifier, in the form of owner/id
        :type project_key: str
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.delete_project(
        ...     'username/test-project')  # doctest: +SKIP
        """
        owner_id, project_id = parse_dataset_key(project_key)
        try:
            self._projects_api.delete_project(owner_id, project_id)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    # Insight Operations

    def get_insight(self, project_key, insight_id, **kwargs):
        """Retrieve an insight

        :param project_key: Project identifier, in the form of
        projectOwner/projectid
        :type project_key: str
        :param insight_id: Insight unique identifier.
        :type insight_id: str
        :returns: Insight definition, with all attributes
        :rtype: object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> insight = api_client.get_insight(
        ...     'jonloyens/'
        ...     'an-example-project-that-shows-what-to-put-in-data-world',
        ...     'c2538b0c-c200-474c-9631-5ff4f13026eb')  # doctest: +SKIP
        >>> insight['title']  # doctest: +SKIP
        'Coast Guard Lives Saved by Fiscal Year'
        """
        try:
            project_owner, project_id = parse_dataset_key(project_key)
            return self._insights_api.get_insight(project_owner,
                                                  project_id,
                                                  insight_id,
                                                  **kwargs).to_dict()
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def get_insights_for_project(self, project_key, **kwargs):
        """Get insights for a project.

        :param project_key: Project identifier, in the form of
        projectOwner/projectid
        :type project_key: str
        :returns: Insight results
        :rtype: object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> insights = api_client.get_insights_for_project(
        ...     'jonloyens/'
        ...     'an-example-project-that-shows-what-to-put-in-data-world'
        ... ) # doctest: +SKIP
        """
        try:
            project_owner, project_id = parse_dataset_key(project_key)
            return self._insights_api.get_insights_for_project(project_owner,
                                                               project_id,
                                                               **kwargs)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def create_insight(self, project_key, **kwargs):
        """Create a new insight

        :param project_key: Project identifier, in the form of
        projectOwner/projectid
        :type project_key: str
        :param title: Insight title
        :type title: str
        :param description: Insight description.
        :type description: str, optional
        :param image_url: If image-based, the URL of the image
        :type image_url: str
        :param embed_url: If embed-based, the embeddable URL
        :type embed_url: str
        :param source_link: Permalink to source code or platform this insight
        was generated with. Allows others to replicate the steps originally
        used to produce the insight.
        :type source_link: str, optional
        :param data_source_links: One or more permalinks to the data sources
        used to generate this insight. Allows others to access the data
        originally used to produce the insight.
        :type data_source_links: array
        :returns: Insight with message and uri object
        :rtype: object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.create_insight(
        ...     'projectOwner/projectid', title='Test insight',
        ...     image_url='url')  # doctest: +SKIP
        """
        request = self.__build_insight_obj(
            lambda: _swagger.InsightCreateRequest(
                title=kwargs.get('title'),
                body=_swagger.InsightBody(
                    image_url=kwargs.get('image_url'),
                    embed_url=kwargs.get('embed_url'),
                    markdown_body=kwargs.get('markdown_body')
                )
            ), kwargs)
        project_owner, project_id = parse_dataset_key(project_key)
        try:
            (_, _, headers) = self._insights_api.create_insight_with_http_info(
                project_owner,
                project_id,
                body=request,
                _return_http_data_only=False)
            if 'Location' in headers:
                return headers['Location']
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def replace_insight(self, project_key, insight_id, **kwargs):
        """Replace an insight.

        :param project_key: Projrct identifier, in the form of
        projectOwner/projectid
        :type project_key: str
        :param insight_id: Insight unique identifier.
        :type insight_id: str
        :param title: Insight title
        :type title: str
        :param description: Insight description.
        :type description: str, optional
        :param image_url: If image-based, the URL of the image
        :type image_url: str
        :param embed_url: If embed-based, the embeddable URL
        :type embed_url: str
        :param source_link: Permalink to source code or platform this insight
        was generated with. Allows others to replicate the steps originally
        used to produce the insight.
        :type source_link: str, optional
        :param data_source_links: One or more permalinks to the data sources
        used to generate this insight. Allows others to access the data
        originally used to produce the insight.
        :type data_source_links: array
        :returns: message object
        :rtype: object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.replace_insight(
        ... 'projectOwner/projectid',
        ... '1230-9324-3424242442',
        ...  embed_url='url',
        ...  title='Test insight')  # doctest: +SKIP
        """
        request = self.__build_insight_obj(
            lambda: _swagger.InsightPutRequest(
                title=kwargs.get('title'),
                body=_swagger.InsightBody(
                    image_url=kwargs.get('image_url'),
                    embed_url=kwargs.get('embed_url'),
                    markdown_body=kwargs.get('markdown_body')
                )
            ), kwargs)
        project_owner, project_id = parse_dataset_key(project_key)
        try:
            self._insights_api.replace_insight(project_owner,
                                               project_id,
                                               insight_id,
                                               body=request)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def update_insight(self, project_key, insight_id, **kwargs):
        """Update an insight.

        **Note that only elements included in the request will be updated. All
        omitted elements will remain untouched.
        :param project_key: Projrct identifier, in the form of
        projectOwner/projectid
        :type project_key: str
        :param insight_id: Insight unique identifier.
        :type insight_id: str
        :param title: Insight title
        :type title: str
        :param description: Insight description.
        :type description: str, optional
        :param image_url: If image-based, the URL of the image
        :type image_url: str
        :param embed_url: If embed-based, the embeddable URL
        :type embed_url: str
        :param source_link: Permalink to source code or platform this insight
        was generated with. Allows others to replicate the steps originally
        used to produce the insight.
        :type source_link: str, optional
        :param data_source_links: One or more permalinks to the data sources
        used to generate this insight. Allows others to access the data
        originally used to produce the insight.
        :type data_source_links: array
        :returns: message object
        :rtype: object
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> api_client.update_insight(
        ...    'username/test-project', 'insightid'
        ...    title='demo atadotworld'})  # doctest: +SKIP
        """
        request = self.__build_insight_obj(
            lambda: _swagger.InsightPatchRequest(), kwargs)
        project_owner, project_id = parse_dataset_key(project_key)
        try:
            self._insights_api.update_insight(project_owner,
                                              project_id,
                                              insight_id, body=request)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    def delete_insight(self, project_key, insight_id):
        """Delete an existing insight.

        :params project_key: Project identifier, in the form of
        projectOwner/projectId
        :type project_key: str
        :params insight_id: Insight unique id
        :type insight_id: str
        :raises RestApiException: If a server error occurs

        Examples
        --------
        >>> import datadotworld as dw
        >>> api_client = dw.api_client()
        >>> del_insight = api_client.delete_insight(
        ...     'username/project', 'insightid')  # doctest: +SKIP
        """
        projectOwner, projectId = parse_dataset_key(project_key)
        try:
            self._insights_api.delete_insight(projectOwner,
                                              projectId,
                                              insight_id)
        except _swagger.rest.ApiException as e:
            raise RestApiError(cause=e)

    @staticmethod
    def __build_dataset_obj(dataset_constructor, file_constructor, args):
        files = ([file_constructor(
            name,
            url=file_info.get('url'),
            expand_archive=file_info.get('expand_archive', False),
            description=file_info.get('description'),
            labels=file_info.get('labels'))
                     for name, file_info in args['files'].items()]
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

    @staticmethod
    def __build_project_obj(project_constructor, file_constructor, args):

        files = ([file_constructor(
            name,
            url=file_info.get('url'),
            description=file_info.get('description'),
            labels=file_info.get('labels'))
                     for name, file_info in args['files'].items()]
                 if 'files' in args else None)
        project = project_constructor()
        if 'title' in args:
            project.title = args['title']
        if 'summary' in args:
            project.summary = args['summary']
        if 'tags' in args:
            project.tags = args['tags']
        if 'license' in args:
            project.license = args['license']
        if 'visibility' in args:
            project.visibility = args['visibility']
        if 'objective' in args:
            project.objective = args['objective']
        if 'linked_datasets' in args:
            project.linked_datasets = args['linked_datasets']

        project.files = files
        return project

    @staticmethod
    def __build_insight_obj(insight_constructor, args):
        insight = insight_constructor()
        if 'title' in args:
            insight.title = args['title']
        if ('image_url' in args or
                'embed_url' in args or
                'markdown_body' in args):
            insight.body = _swagger.InsightBody(
                image_url=args.get('image_url'),
                embed_url=args.get('embed_url'),
                markdown_body=args.get('markdown_body')
            )
        if 'description' in args:
            insight.description = args['description']
        if 'source_link' in args:
            insight.source_link = args['source_link']
        if 'data_source_links' in args:
            insight.data_source_links = args['data_source_links']
        return insight


class RestApiError(Exception):
    """Exception wrapper for errors raised by requests or by
    the swagger client"""

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

        Data.world often includes a JSON body for errors;
        however, there are no guarantees.

        :returns: The JSON body if one is included. Otherwise, None.
        :rtype: dict (json)
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
