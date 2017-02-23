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
from doublex import Stub, assert_that
from hamcrest import has_entries, equal_to

from datadotworld.config import Config


class Helpers(object):
    @staticmethod
    def validate_request_headers(token='token', user_agent=None):
        from datadotworld import __version__
        expected_ua_header = user_agent or 'data.world-py - {}'.format(__version__)
        expected_auth_header = 'Bearer {}'.format(token)

        def wrap(f):
            def wrapper(request):
                headers = request.headers
                assert_that(headers, has_entries({'Authorization': equal_to(expected_auth_header),
                                                  'User-Agent': equal_to(expected_ua_header)}))
                return f(request)

            return wrapper

        return wrap


@pytest.fixture()
def helpers():
    return Helpers


@pytest.fixture(params=['agentid/datasetid', 'https://data.world/agentid/datasetid'], ids=['simple_key', 'url'])
def dataset_key(request):
    return request.param


@pytest.fixture()
def config(tmpdir):
    with Stub(Config) as cfg:
        cfg.auth_token = 'token'
        cfg.tmp_dir = path.join(str(tmpdir), 'tmp')
        if not path.isdir(path.dirname(cfg.tmp_dir)):
            os.makedirs(path.dirname(cfg.tmp_dir))
        cfg.cache_dir = path.join(str(tmpdir), 'cache')
        if not path.isdir(path.dirname(cfg.cache_dir)):
            os.makedirs(path.dirname(cfg.cache_dir))
        return cfg


@pytest.fixture()
def query_result_csv():
    return u'cool,beans\n1,2\n3,4\n'


@pytest.fixture()
def test_files_path():
    root_dir = path.dirname(path.abspath(__file__))
    return path.join(root_dir, 'fixtures')
