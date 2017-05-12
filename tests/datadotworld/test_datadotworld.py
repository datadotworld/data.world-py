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

from __future__ import absolute_import

import json
import os
import re
import shutil
import warnings
from os import path

import pytest
import responses
from doublex import assert_that, Spy, when, called, never, Stub
from hamcrest import equal_to, calling, raises, has_length, anything, is_

import datadotworld
from datadotworld.client.api import RestApiClient, RestApiError
from datadotworld.datadotworld import DataDotWorld


class TestDataDotWorld:
    @pytest.fixture()
    def query_response_json(self, test_queries_path):
        with open(path.join(test_queries_path, 'sql_select.json'),
                  'r') as json_results:
            return json.load(json_results)

    @pytest.fixture()
    def existing_dataset(self, config, test_datapackages_path):
        # Previously downloaded
        dest_dir = path.join(config.cache_dir, 'agentid', 'datasetid',
                             'latest')
        shutil.copytree(
            path.join(test_datapackages_path,
                      'the-simpsons-by-the-data-existing'),
            dest_dir)

    @pytest.fixture()
    def api_client(self, test_datapackages_path):
        with Spy(RestApiClient) as client:
            def download_datapackage(_, dest_dir):
                shutil.copytree(
                    path.join(test_datapackages_path,
                              'the-simpsons-by-the-data'),
                    dest_dir)
                return path.join(dest_dir, 'datapackage.json')

            def get_dataset(_):
                return {'updated': '2016-11-07T00:00:00.000Z'}

            client.download_datapackage(anything(), anything()).delegates(
                download_datapackage)
            client.get_dataset(anything()).delegates(
                get_dataset)
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
                   query_response_json):
        with responses.RequestsMock() as rsps:
            @helpers.validate_request_headers()
            def query_endpoint(_):
                return 200, {}, json.dumps(query_response_json)

            rsps.add_callback(rsps.GET, '{}?query={}'.format(endpoint, query),
                              content_type='text/csv',
                              callback=query_endpoint, match_querystring=True)

            result = dw.query(dataset_key, query, query_type=type)
            assert_that(result.raw_data, equal_to(query_response_json))

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

    parameterized_queries = [
        ('sql', 'notreallysql', ["USA", 10, 100.0, False],
         'https://query.data.world/sql/agentid/datasetid?'
         'query=notreallysql&'
         'parameters='
         '%24data_world_param3%3D%22False%22%5E%5E%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23boolean%3E%2C'
         '%24data_world_param2%3D%22100.0%22%5E%5E%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23decimal%3E%2C'
         '%24data_world_param1%3D%2210%22%5E%5E%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23integer%3E%2C'
         '%24data_world_param0%3D%22USA%22'
         ),
        ('sparql', 'notreallysparql', {'$aString': "USA", '$anInt': 10, '$aDecimal': 100.0, '$aBool': False},
         'https://query.data.world/sparql/agentid/datasetid?'
         'query=notreallysparql&'
         'parameters='
         '%24anInt%3D%2210%22%5E%5E%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23integer%3E%2C'
         '%24aDecimal%3D%22100.0%22%5E%5E%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23decimal%3E%2C'
         '%24aString%3D%22USA%22%2C'
         '%24aBool%3D%22False%22%5E%5E%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23boolean%3E'
         )
    ]

    @pytest.mark.parametrize("type,query,parameters,expected", parameterized_queries)
    def test_parameterized_queries(self, type, query, parameters, expected,
                                   dw, dataset_key, query_response_json):
        with responses.RequestsMock() as rsps:
            def request_callback(request):
                assert_that(request.url, equal_to(expected),
                            reason="Expected [[\n{}\n]] got [[\n{}\n]]".format(expected, request.url))
                return(200, {}, json.dumps(query_response_json))

            rsps.add_callback(rsps.GET, re.compile(r'https?://query\.data\.world/.*'),
                              callback = request_callback, content_type="application/json",
                              match_querystring=True)

            dw.query(dataset_key, query, query_type=type, parameters=parameters)

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
        with warnings.catch_warnings(record=True) as w:
            dataset = dw.load_dataset(dataset_key)
            assert_that(w, has_length(0))
        assert_that(api_client.download_datapackage, never(called()))
        assert_that(dataset.raw_data, has_length(3))

    @pytest.mark.usefixtures('existing_dataset')
    def test_load_dataset_existing_expired(self, monkeypatch, api_client, dw,
                                           dataset_key):
        monkeypatch.setattr(os.path, 'getmtime', lambda _: 1468195199)
        with warnings.catch_warnings(record=True) as w:
            dataset = dw.load_dataset(dataset_key)
            assert_that(w, has_length(1))
            assert_that(w[-1].category, equal_to(UserWarning))

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
    import datadotworld
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
