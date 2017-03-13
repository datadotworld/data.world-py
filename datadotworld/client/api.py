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
from __future__ import absolute_import, division

import json
import os
import shutil
import uuid
import zipfile
from os import path

import progressbar
import requests

from datadotworld.client import _swagger
from datadotworld.config import Config
from datadotworld.util import parse_dataset_key, _user_agent, interactive_mode_enabled


class RestApiClient:
    """A Python Client for data.world's REST API"""

    def __init__(self, profile='default', **kwargs):
        self._config = Config(profile)

        # Overrides for testing
        self._protocol = kwargs.get('protocol', 'https')
        self._download_host = kwargs.get('download_host', 'download.data.world')

        api_host = kwargs.get('api_host', 'api.data.world')
        swagger_client = _swagger.ApiClient(host="{}://{}/v0".format(self._protocol, api_host),
                                            header_name='Authorization',
                                            header_value='Bearer {}'.format(self._config.auth_token))
        swagger_client.user_agent = _user_agent()

        self._datasets_api = _swagger.DatasetsApi(swagger_client)
        self._uploads_api = _swagger.UploadsApi(swagger_client)

    # Dataset Operations

    def get_dataset(self, dataset_key):
        """Retrieve an existing dataset

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
        >>> api_client = datadotworld.api_client()
        >>> intro_dataset = api_client.get_dataset('jonloyens/an-intro-to-dataworld-dataset')
        >>> print(intro_dataset['description'])
        A dataset that serves as a quick introduction to data.world and some of our capabilities.  Follow along in \
        the summary!
        """
        try:
            return self._datasets_api.get_dataset(*(parse_dataset_key(dataset_key))).to_dict()
        except _swagger.ApiException as e:
            raise RestApiError(cause=e)

    def create_dataset(self, owner_id, **kwargs):
        """Create a new dataset

        Parameters
        ----------
        owner_id : str
            Username of the owner of the new dataset
        title : str
            Dataset title
        description : str, optional
            Dataset description
        summary : str, optional
            Dataset summary markdown
        tags : list, optional
            Dataset tags
        license : {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY', 'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 
                   'CC BY-NC-SA', 'Other'}
            Dataset license
        visibility : {'OPEN', 'PRIVATE'}
            Dataset visibility
        files : dict
            File names and source URLs

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> intro_dataset = {}
        >>> intro_dataset['title'] = 'An intro to data.world dataset'
        >>> intro_dataset['visibility'] = 'OPEN'
        >>> intro_dataset['license'] = 'Public Domain License'
        >>> api_client = datadotworld.api_client()
        >>> api_client.create_dataset('jonloyens', **intro_dataset)
        """
        request = self.__build_dataset(lambda: _swagger.DatasetCreateRequest(),
                                       lambda name, url: _swagger.FileCreateRequest(
                                           name=name, source=_swagger.FileSourceCreateRequest(url=url)),
                                       kwargs)

        try:
            self._datasets_api.create_dataset(owner_id, request)
        except _swagger.ApiException as e:
            raise RestApiError(cause=e)

    def patch_dataset(self, dataset_key, **kwargs):
        """Update an existing dataset

        Parameters
        ----------
        description : str, optional
            Dataset description
        summary : str, optional
            Dataset summary markdown
        tags : list, optional
            Dataset tags
        license : {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY', 'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 
                   'CC BY-NC-SA', 'Other'}, optional
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
        >>> intro_dataset_patch = {}
        >>> intro_dataset_patch['tags'] = ['demo', 'datadotworld']
        >>> api_client = datadotworld.api_client()
        >>> api_client.patch_dataset('jonloyens/an-intro-to-dataworld-dataset', intro_dataset_patch)
        """
        request = self.__build_dataset(lambda: _swagger.DatasetPatchRequest(),
                                       lambda name, url: _swagger.FileCreateOrUpdateRequest(
                                           name=name, source=_swagger.FileSourceCreateOrUpdateRequest(url=url)),
                                       kwargs)

        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.patch_dataset(owner_id, dataset_id, request)
        except _swagger.ApiException as e:
            raise RestApiError(cause=e)

    def replace_dataset(self, dataset_key, **kwargs):
        """Replace an existing dataset

        *This method will completely overwrite an existing dataset.*

        Parameters
        ----------
        description : str, optional
            Dataset description
        summary : str, optional
            Dataset summary markdown
        tags : list, optional
            Dataset tags
        license : {'Public Domain', 'PDDL', 'CC-0', 'CC-BY', 'ODC-BY', 'CC-BY-SA', 'ODC-ODbL', 'CC BY-NC', 
                   'CC BY-NC-SA', 'Other'}
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
        >>> intro_dataset_overwrite = {}
        >>> intro_dataset_overwrite['description'] = 'A dataset that serves as a quick introduction to data.world'
        >>> intro_dataset_overwrite['tags'] = ['demo', 'datadotworld']
        >>> intro_dataset_overwrite['visibility']='OPEN'
        >>> intro_dataset_overwrite['license'] = 'Other'
        >>> api_client = datadotworld.api_client()
        >>> api_client.replace_dataset('jonloyens/an-intro-to-dataworld-dataset', intro_dataset_overwrite)
        """
        request = self.__build_dataset(lambda: _swagger.DatasetPutRequest(),
                                       lambda name, url: _swagger.FileCreateRequest(
                                           name=name, source=_swagger.FileSourceCreateRequest(url=url)),
                                       kwargs)

        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.replace_dataset(owner_id, dataset_id, request)
        except _swagger.ApiException as e:
            raise RestApiError(cause=e)

    # File Operations

    def add_files_via_url(self, dataset_key, files={}):
        """Add or update dataset files linked to source URLs

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        files : dict
            File names and source URLs to add or update

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> api_client = datadotworld.api_client()
        >>> api_client.add_files_via_url('jonloyens/an-intro-to-dataworld-dataset',  
        >>>    {'atx_startup_league_ranking.csv': 'http://www.atxsa.com/sports/basketball/startup_league_ranking.csv'})
        """
        file_requests = [_swagger.FileCreateOrUpdateRequest(
            name=name, source=_swagger.FileSourceCreateOrUpdateRequest(url=url)) for name, url in files.items()]

        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.add_files_by_source(owner_id, dataset_id,
                                                   _swagger.FileBatchUpdateRequest(files=file_requests))
        except _swagger.ApiException as e:
            raise RestApiError(cause=e)

    def sync_files(self, dataset_key):
        """Trigger synchronization process to update all dataset files linked to source URLs

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
        >>> api_client = datadotworld.api_client()
        >>> api_client.sync_files('jonloyens/an-intro-to-dataworld-dataset')
        """
        try:
            self._datasets_api.sync(*(parse_dataset_key(dataset_key)))
        except _swagger.ApiException as e:
            raise RestApiError(cause=e)

    def upload_files(self, dataset_key, files):
        """Upload dataset files

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        files : list of str
            The list of names/paths for files stored in the local filesystem

        Raises
        ------
        RestApiException
            If a server error occurs

        Examples
        --------
        >>> api_client = datadotworld.api_client()
        >>> api_client.upload_files('jonloyens/an-intro-to-dataworld-dataset',
        >>>                 ['/Users/jon/DataDotWorldBBall/DataDotWorldBBallTeam.csv'])
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._uploads_api.upload_files(owner_id, dataset_id, files)
        except _swagger.ApiException as e:
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
        >>> api_client = datadotworld.api_client()
        >>> api_client.delete_files('jonloyens/an-intro-to-dataworld-dataset', ['atx_startup_league_ranking.csv'])
        """
        owner_id, dataset_id = parse_dataset_key(dataset_key)
        try:
            self._datasets_api.delete_files_and_sync_sources(owner_id, dataset_id, names)
        except _swagger.ApiException as e:
            raise RestApiError(cause=e)

    # Datapackage

    def download_datapackage(self, dataset_key, dest_dir):
        """Download and unzip a dataset's data package

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id
        dest_dir : str or path
            Directory under which datapackage should be saved

        Returns
        -------
        path
            Location of the datapackage descriptor (datapackage.json) in the local filesystem

        Raises
        ------
        RestApiException
            If a server error occurs
        """
        url = "{0}://{1}/datapackage/{2}".format(self._protocol, self._download_host, dataset_key)
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

        content_length = (response.headers.get('content-length') or
                          len(response.content) if response.content is not None else None)

        with open(zip_file, 'wb') as f:
            for data in self.__interactive_progress_info(response.iter_content(chunk_size=4096), 4096, content_length):
                f.write(data)

        zip_obj = zipfile.ZipFile(zip_file)
        zip_obj.extractall(path=unzip_dir)
        unzipped_dir = [path.join(unzip_dir, d) for d in os.listdir(unzip_dir)
                        if path.isdir(path.join(unzip_dir, d))][0]

        shutil.move(unzipped_dir, dest_dir)

        if interactive_mode_enabled():
            print('Saved at: {}'.format(dest_dir))

        return path.join(dest_dir, 'datapackage.json')

    @staticmethod
    def __build_dataset(dataset_constructor, file_constructor, args):
        files = [file_constructor(name, url)
                 for name, url in args['files'].items()] if 'files' in args else None

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
    def __interactive_progress_info(iterable, chunk_size=1, total_size=None):
        if interactive_mode_enabled():
            # Show progress bar in interactive mode
            bar = progressbar.ProgressBar(max_value=int(total_size) or progressbar.UnknownLength,
                                          widgets=[progressbar.DataSize()])

            for x in iterable:
                yield x
                if bar.max_value == progressbar.UnknownLength or (bar.max_value - bar.value) > chunk_size:
                    bar.update(bar.value + chunk_size)
                else:
                    bar.update(bar.max_value)
        else:
            return iter


class RestApiError(Exception):
    def __init__(self, *args, **kwargs):
        if 'cause' in kwargs:
            cause = kwargs.pop('cause')
            if type(cause) is _swagger.ApiException:
                self.status = cause.status
                self.reason = cause.reason
                self.body = cause.body
            elif type(cause) is requests.RequestException:
                requests_response = cause.response
                if requests_response is not None:
                    self.status = requests_response.status_code
                    self.reason = requests_response.reason
                    self.body = requests_response.content
                    self.json = requests_response.json  # Delegates to requests

        self.status = kwargs.pop('status', None)
        self.reason = kwargs.pop('reason', None)
        self.body = kwargs.pop('body', None)
        super(RestApiError, self).__init__(*args, **kwargs)

    def json(self):
        try:
            return json.loads(self.body)
        except json.JSONDecodeError:
            raise ValueError('Error response body is not a valid JSON')

    def __str__(self):
        return str(self.json() or self.body)
