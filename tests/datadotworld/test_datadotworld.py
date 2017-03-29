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

import json
import shutil
from os import path

import pytest
import responses
from doublex import assert_that, Spy, when, called, never, Stub
from hamcrest import equal_to, calling, raises, has_length, anything, is_

from datadotworld import datadotworld
from datadotworld.client.api import RestApiClient, RestApiError
from datadotworld.datadotworld import DataDotWorld


class TestDataDotWorld:
    @pytest.fixture()
    def existing_dataset(self, config, test_files_path):
        # Previously downloaded
        dest_dir = path.join(config.cache_dir, 'agentid', 'datasetid',
                             'latest')
        shutil.copytree(
            path.join(test_files_path, 'the-simpsons-by-the-data-existing'),
            dest_dir)

    @pytest.fixture()
    def api_client(self, test_files_path):
        with Spy(RestApiClient) as client:
            def download_datapackage(_, dest_dir):
                shutil.copytree(
                    path.join(test_files_path, 'the-simpsons-by-the-data'),
                    dest_dir)
                return path.join(dest_dir, 'datapackage.json')

            client.download_datapackage(anything(), anything()).delegates(
                download_datapackage)
            return client

    @pytest.fixture()
    def dw(self, config, api_client):
        dw = DataDotWorld(config=config)
        dw.api_client = api_client
        return dw

    query_types = [
        # Using proper queries here trips the responses framework when they
        # are url-encoded and causes tests to fail
        ('sparql', 'https://query.data.world/sparql/agentid/datasetid',
         'notreallysparql'),
        ('sql', 'https://query.data.world/sql/agentid/datasetid',
         'notreallysql')
    ]

    @pytest.mark.parametrize("type,endpoint,query", query_types,
                             ids=['sparql', 'sql'])
    def test_query(self, helpers, dw, dataset_key, type, endpoint, query,
                   query_result_json):
        with responses.RequestsMock() as rsps:
            @helpers.validate_request_headers()
            def query_endpoint(_):
                return 200, {}, json.dumps(query_result_json)

            rsps.add_callback(rsps.GET, '{}?query={}'.format(endpoint, query),
                              content_type='text/csv',
                              callback=query_endpoint, match_querystring=True)

            result = dw.query(dataset_key, query, query_type=type)
            assert_that(result.raw_data, equal_to(query_result_json))

    @pytest.mark.parametrize("type,endpoint,query", query_types,
                             ids=['sparql', 'sql'])
    def test_query_400(self, dw, dataset_key, type, endpoint, query):
        with responses.RequestsMock() as rsps:
            rsps.add(rsps.GET, '{}?query={}'.format(endpoint, query),
                     match_querystring=True,
                     status=400)

            assert_that(calling(dw.query).with_args(dataset_key, query,
                                                    query_type=type),
                        raises(RuntimeError))

    def test_load_dataset(self, config, api_client, dw, dataset_key):
        dest_dir = path.join(config.cache_dir, 'agentid', 'datasetid',
                             'latest')
        assert_that(path.isdir(dest_dir), is_(False))

        dataset = dw.load_dataset(dataset_key)

        assert_that(api_client.download_datapackage,
                    called().times(1).with_args(equal_to(dataset_key),
                                                equal_to(dest_dir)))
        assert_that(dataset.raw_data, has_length(4))

    @pytest.mark.usefixtures('existing_dataset')
    def test_load_dataset_existing(self, api_client, dw, dataset_key):
        dataset = dw.load_dataset(dataset_key)

        assert_that(api_client.download_datapackage, never(called()))
        assert_that(dataset.raw_data, has_length(3))

    @pytest.mark.usefixtures('existing_dataset')
    def test_load_dataset_existing_forced(self, api_client, dw, dataset_key):
        dataset = dw.load_dataset(dataset_key, force_update=True)

        assert_that(api_client.download_datapackage,
                    called().times(1).with_args(equal_to(dataset_key),
                                                anything()))
        assert_that(dataset.raw_data, has_length(4))

    @pytest.mark.usefixtures('existing_dataset')
    def test_load_dataset_forced_fallback(self, api_client, dw, dataset_key):
        when(api_client).download_datapackage(equal_to(dataset_key),
                                              anything()).raises(RestApiError)

        # Forced update
        dataset = dw.load_dataset(dataset_key, force_update=True)
        assert_that(api_client.download_datapackage,
                    called().times(1).with_args(equal_to(dataset_key),
                                                anything()))
        assert_that(dataset.raw_data, has_length(3))


# Top-level methods

@pytest.fixture()
def dw_instances(monkeypatch):
    from datadotworld import datadotworld
    with Spy(DataDotWorld) as dw, Spy(DataDotWorld) as dw_alternative:
        dw.api_client = dw_alternative.api_client = Stub(RestApiClient)
        monkeypatch.setattr(
            datadotworld, '_get_instance',
            lambda profile: dw if profile == 'default' else dw_alternative)
        return {'default': dw, 'alternative': dw_alternative}


@pytest.fixture(params=['default', 'alternative'],
                ids=['default', 'alternative'])
def profile(request):
    return request.param


def test_toplevel_load_dataset(dw_instances, profile):
    datadotworld.load_dataset('agentid/datasetid', profile=profile)
    assert_that(dw_instances[profile].load_dataset,
                called().times(1).with_args(equal_to('agentid/datasetid'),
                                            force_update=equal_to(False)))


def test_toplevel_query(dw_instances, profile):
    datadotworld.query('agentid/datasetid', 'SELECT * FROM Tables',
                       profile=profile)
    assert_that(dw_instances[profile].query,
                called().times(1).with_args(equal_to('agentid/datasetid'),
                                            equal_to('SELECT * FROM Tables'),
                                            query_type=equal_to('sql')))


def test_toplevel_api_client(dw_instances, profile):
    assert_that(datadotworld.api_client(),
                equal_to(dw_instances[profile].api_client))
