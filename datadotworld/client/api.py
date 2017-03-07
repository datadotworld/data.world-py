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

from datadotworld.client import _swagger
from datadotworld.config import Config
from datadotworld.util import split_dataset_key, user_agent


class RestApiClient:
    """A Python Client for data.world's REST API"""

    def __init__(self, profile='default', **kwargs):
        config = Config(profile)

        # Overrides for testing
        protocol = kwargs.get('protocol', 'https')
        api_host = kwargs.get('api_host', 'api.data.world')

        api_client = _swagger.ApiClient(host="{}://{}/v0".format(protocol, api_host), header_name='Authorization',
                                        header_value='Bearer {}'.format(config.auth_token))
        api_client.user_agent = user_agent()

        self._datasets_api = _swagger.DatasetsApi(api_client)
        self._uploads_api = _swagger.UploadsApi(api_client)

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
        ApiException
            If a server error occurs

        Examples
        --------
        >>> api_client = datadotworld.api_client()
        >>> intro_dataset = api_client.get_dataset('jonloyens/an-intro-to-dataworld-dataset')
        >>> print(intro_dataset['description'])
        A dataset that serves as a quick introduction to data.world and some of our capabilities.  Follow along in \
        the summary!
        """
        return self._datasets_api.get_dataset(*(split_dataset_key(dataset_key))).to_dict()

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
        ApiException
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

        self._datasets_api.create_dataset(owner_id, request)

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
        ApiException
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

        owner_id, dataset_id = split_dataset_key(dataset_key)
        self._datasets_api.patch_dataset(owner_id, dataset_id, request)

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
        ApiException
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

        owner_id, dataset_id = split_dataset_key(dataset_key)
        self._datasets_api.replace_dataset(owner_id, dataset_id, request)

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
        ApiException
            If a server error occurs

        Examples
        --------
        >>> api_client = datadotworld.api_client()
        >>> api_client.add_files_via_url('jonloyens/an-intro-to-dataworld-dataset',  
        >>>    {'atx_startup_league_ranking.csv': 'http://www.atxsa.com/sports/basketball/startup_league_ranking.csv'})
        """
        file_requests = [_swagger.FileCreateOrUpdateRequest(
            name=name, source=_swagger.FileSourceCreateOrUpdateRequest(url=url)) for name, url in files.items()]

        owner_id, dataset_id = split_dataset_key(dataset_key)
        self._datasets_api.add_files_by_source(owner_id, dataset_id,
                                               _swagger.FileBatchUpdateRequest(files=file_requests))

    def sync_files(self, dataset_key):
        """Trigger synchronization process to update all dataset files linked to source URLs

        Parameters
        ----------
        dataset_key : str
            Dataset identifier, in the form of owner/id

        Raises
        ------
        ApiException
            If a server error occurs

        Examples
        --------
        >>> api_client = datadotworld.api_client()
        >>> api_client.sync_files('jonloyens/an-intro-to-dataworld-dataset')
        """
        self._datasets_api.sync(*(split_dataset_key(dataset_key)))

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
        ApiException
            If a server error occurs

        Examples
        --------
        >>> api_client = datadotworld.api_client()
        >>> api_client.upload_files('jonloyens/an-intro-to-dataworld-dataset',
        >>>                 ['/Users/jon/DataDotWorldBBall/DataDotWorldBBallTeam.csv'])
        """
        owner_id, dataset_id = split_dataset_key(dataset_key)
        self._uploads_api.upload_files(owner_id, dataset_id, files)

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
        ApiException
            If a server error occurs

        Examples
        --------
        >>> api_client = datadotworld.api_client()
        >>> api_client.delete_files('jonloyens/an-intro-to-dataworld-dataset', ['atx_startup_league_ranking.csv'])
        """
        owner_id, dataset_id = split_dataset_key(dataset_key)
        self._datasets_api.delete_files_and_sync_sources(owner_id, dataset_id, names)

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
