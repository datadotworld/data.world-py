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
from os import path

import pytest
import responses
from doublex import assert_that, Spy, called
from hamcrest import equal_to, has_entries, has_properties, is_, described_as, empty, raises, calling

from datadotworld.client._swagger import DatasetsApi, UploadsApi
from datadotworld.client._swagger.models import *
from datadotworld.client.api import RestApiClient, RestApiError


class TestApiClient:
    @pytest.fixture()
    def datasets_api(self):
        with Spy(DatasetsApi) as api:
            api.get_dataset = lambda o, d: DatasetSummaryResponse(o, d)
            return api

    @pytest.fixture()
    def uploads_api(self):
        with Spy(UploadsApi) as api:
            api.get_dataset = lambda o, d: DatasetSummaryResponse(o, d)
            return api

    @pytest.fixture()
    def api_client(self, config, datasets_api, uploads_api):
        client = RestApiClient(config)
        client._datasets_api = datasets_api
        client._uploads_api = uploads_api
        return client

    def test_get_dataset(self, api_client, dataset_key):
        dataset = api_client.get_dataset(dataset_key)
        assert_that(dataset, has_entries({'owner': equal_to('agentid'), 'id': equal_to('datasetid')}))

    def test_create_dataset(self, api_client, datasets_api):
        create_request = {'title': 'Dataset', 'visibility': 'OPEN', 'license': 'Public Domain'}
        api_client.create_dataset('agentid', **create_request)
        assert_that(datasets_api.create_dataset,
                    called().times(1).with_args(equal_to('agentid'), has_properties(create_request)))

    def test_patch_dataset(self, api_client, datasets_api, dataset_key):
        patch_request = {'tags': ['tag1', 'tag2']}
        api_client.patch_dataset(dataset_key, **patch_request)
        assert_that(datasets_api.patch_dataset,
                    called().times(1).with_args(equal_to('agentid'),
                                                equal_to('datasetid'), has_properties(patch_request)))

    def test_replace_dataset(self, api_client, datasets_api, dataset_key):
        replace_request = {'visibility': 'OPEN'}
        api_client.replace_dataset(dataset_key, **replace_request)
        assert_that(datasets_api.replace_dataset,
                    called().times(1).with_args(equal_to('agentid'),
                                                equal_to('datasetid'), has_properties(replace_request)))

    def test_add_files_via_url(self, api_client, datasets_api, dataset_key):
        file_update_request = {'filename.ext': 'https://acme.inc/filename.ext'}
        file_update_object = FileBatchUpdateRequest(
            files=[FileCreateOrUpdateRequest(name='filename.ext', source=FileSourceCreateOrUpdateRequest(
                url='https://acme.inc/filename.ext'))])

        api_client.add_files_via_url(dataset_key, file_update_request)
        assert_that(datasets_api.add_files_by_source,
                    called().times(1).with_args(equal_to('agentid'),
                                                equal_to('datasetid'), equal_to(file_update_object)))

    def test_sync_files(self, api_client, datasets_api, dataset_key):
        api_client.sync_files(dataset_key)
        assert_that(datasets_api.sync, called().times(1).with_args('agentid', 'datasetid'))

    def test_upload_files(self, api_client, uploads_api, dataset_key):
        files = ['filename.ext']
        api_client.upload_files(dataset_key, files)
        assert_that(uploads_api.upload_files,
                    called().times(1).with_args(equal_to('agentid'), equal_to('datasetid'), equal_to(files)))

    def test_delete_files(self, api_client, datasets_api, dataset_key):
        files = ['filename.ext']
        api_client.delete_files(dataset_key, files)
        assert_that(datasets_api.delete_files_and_sync_sources,
                    called().times(1).with_args(equal_to('agentid'), equal_to('datasetid'), equal_to(files)))

    # TODO Test CRUD exception cases

    def test_download_datapackage(self, helpers, config, test_files_path, api_client, dataset_key):
        datapackage_zip = path.join(test_files_path, 'the-simpsons-by-the-data.zip')
        with responses.RequestsMock() as rsps, open(datapackage_zip, 'rb') as file:
            @helpers.validate_request_headers()
            def datapackage_endpoint(_):
                return 200, {}, file.read()

            rsps.add_callback(rsps.GET, 'https://download.data.world/datapackage/agentid/datasetid',
                              datapackage_endpoint)

            datapackage = api_client.download_datapackage(dataset_key, config.cache_dir)

            assert_that(datapackage, equal_to(path.join(config.cache_dir, 'datapackage.json')))
            assert_that(path.isfile(datapackage), described_as('%0 is a file', is_(True), datapackage))

            data_subdirectory = path.join(config.cache_dir, 'data')
            assert_that(path.isdir(data_subdirectory), described_as('%0 is a directory', is_(True), data_subdirectory))
            assert_that(os.listdir(config.tmp_dir), described_as('%0 is empty', empty(), config.tmp_dir))

    def test_download_datapackage_error(self, helpers, config, test_files_path, api_client, dataset_key):
        datapackage_zip = path.join(test_files_path, 'the-simpsons-by-the-data.zip')
        with responses.RequestsMock() as rsps, open(datapackage_zip, 'rb') as file:
            @helpers.validate_request_headers()
            def datapackage_endpoint(_):
                return 400, {}, ''

            rsps.add_callback(rsps.GET, 'https://download.data.world/datapackage/agentid/datasetid',
                              datapackage_endpoint)

            assert_that(calling(api_client.download_datapackage).with_args(dataset_key, config.cache_dir),
                        raises(RestApiError))
