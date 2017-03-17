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
data.world, Inc.(http://www.data.world/).
"""
from __future__ import absolute_import

import pytest
from doublex import assert_that
from hamcrest import equal_to, calling, raises, only_contains

from datadotworld import util


def test_parse_dataset_key():
    path_owner, path_id = util.parse_dataset_key('owner/dataset')
    assert_that(path_owner, equal_to('owner'))
    assert_that(path_id, equal_to('dataset'))


def test_parse_dataset_key_with_url():
    url_owner, url_id = util.parse_dataset_key(
        'https://data.world/owner/dataset')
    assert_that(url_owner, equal_to('owner'))
    assert_that(url_id, equal_to('dataset'))


def test_parse_dataset_key_with_bad_path():
    assert_that(calling(util.parse_dataset_key).with_args(
        'owner/dataset/somethingelse'), raises(ValueError))


def test_parse_dataset_key_with_bad_url():
    assert_that(calling(util.parse_dataset_key).with_args(
        'ftp://data.world/owner/dataset'), raises(ValueError))


def test__user_agent():
    from datadotworld import __version__
    assert_that(util._user_agent(),
                equal_to('data.world-py - {}'.format(__version__)))


class TestLazyLoadedDict:
    @pytest.fixture()
    def dict_keys(self):
        return ['key1', 'key2']

    @pytest.fixture()
    def loader_fn(self):
        return lambda key: '{}-value'.format(key)

    @pytest.fixture()
    def lazy_dict(self, dict_keys, loader_fn):
        lazy_dict = util.LazyLoadedDict(dict_keys, loader_fn, type_hint='str')
        return lazy_dict

    def test_get(self, lazy_dict):
        assert_that(lazy_dict['key1'], equal_to('key1-value'))

    def test_get_error(self, lazy_dict):
        assert_that(calling(lambda: lazy_dict['missingkey']), raises(KeyError))

    def test_iter(self, lazy_dict, dict_keys):
        assert_that(iter(lazy_dict), only_contains(*dict_keys))

    def test_repr(self, lazy_dict):
        assert_that(repr(lazy_dict), equal_to(
            '<datadotworld.util.LazyLoadedDict with values of type: str>'))

    def test_str_loaded(self, lazy_dict, dict_keys, loader_fn):
        # Force loading of values
        for _ in lazy_dict.values():
            pass

        expected_values = (repr(loader_fn(k)) for k in dict_keys)
        assert_that(str(lazy_dict),
                    equal_to("{{'key1': {0}, 'key2': {1}}}".format(
                        *expected_values)))

    def test_str_unloaded(self, lazy_dict):
        assert_that(str(lazy_dict),
                    equal_to("{{'key1': {0}, 'key2': {0}}}".format('<str>')))
