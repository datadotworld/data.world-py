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

import configparser
import os
from os import path

import pytest
from doublex import assert_that
from hamcrest import equal_to, is_not, is_, calling, raises, has_length
from six import StringIO

from datadotworld.config import Config


class TestConfig:
    # Fixtures

    @pytest.fixture()
    def config_file_path(self, tmpdir):
        return str(tmpdir.join('.dw/config'))

    @pytest.fixture()
    def legacy_file_path(self, tmpdir):
        return str(tmpdir.join('.data.world'))

    @pytest.fixture()
    def config_directory(self, tmpdir):
        return os.makedirs(str(tmpdir.join('.dw')))

    @pytest.fixture()
    def default_config_file(self, config_file_path):
        config_parser = configparser.ConfigParser()
        config_parser.set(configparser.DEFAULTSECT, 'auth_token', 'abcd')
        config_parser.write(open(config_file_path, 'w'))

    @pytest.fixture()
    def default_invalid_config_file(self, config_file_path):
        config_parser = configparser.ConfigParser()
        config_parser.read_file(StringIO('[default]'))
        config_parser.set('default', 'auth_token', 'lower_case_default')
        config_parser.write(open(config_file_path, 'w'))

    @pytest.fixture()
    def alternative_config_file(self, config_file_path):
        config_parser = configparser.ConfigParser()
        config_parser.add_section('alternative')
        config_parser.set('alternative', 'auth_token', 'alternativeabcd')
        config_parser.write(open(config_file_path, 'w'))

    @pytest.fixture()
    def legacy_config_file(self, legacy_file_path):
        with open(legacy_file_path, 'w') as legacy_file:
            legacy_file.write('token=legacyabcd')

    # Tests

    @pytest.mark.usefixtures('config_directory', 'default_config_file')
    def test_auth_token(self, config_file_path):
        config = Config(config_file_path=config_file_path)
        assert_that(config.auth_token, equal_to('abcd'))

    @pytest.mark.usefixtures('config_directory', 'alternative_config_file')
    def test_alternative_token(self, config_file_path):
        config = Config(profile='alternative',
                        config_file_path=config_file_path)
        assert_that(config.auth_token, equal_to('alternativeabcd'))

    @pytest.mark.usefixtures('legacy_config_file')
    def test_legacy_token(self, legacy_file_path, config_file_path):
        assert_that(path.isfile(config_file_path), is_(False))
        config = Config(legacy_file_path=legacy_file_path,
                        config_file_path=config_file_path)
        assert_that(config.auth_token, equal_to('legacyabcd'))
        assert_that(path.isfile(config_file_path), is_(True))

    @pytest.mark.usefixtures('config_directory', 'default_invalid_config_file')
    def test_invalid_config_section(self, config_file_path):
        config = Config(config_file_path=config_file_path)
        assert_that(config.auth_token, equal_to('lower_case_default'))
        assert_that(config._config_parser.sections(), has_length(0))

    def test_missing_file(self, config_file_path):
        assert_that(path.isfile(config_file_path), is_(False))
        config = Config(config_file_path=config_file_path)
        assert_that(calling(lambda: config.auth_token), raises(RuntimeError))

    @pytest.mark.usefixtures('config_directory', 'default_config_file')
    def test_missing_token(self, config_file_path):
        assert_that(path.isfile(config_file_path), is_(True))
        config = Config(profile='missingprofile',
                        config_file_path=config_file_path)
        assert_that(calling(lambda: config.auth_token), raises(RuntimeError))

    def test_save(self, config_file_path):
        assert_that(path.isfile(config_file_path), is_(False))
        config = Config(config_file_path=config_file_path)
        config.auth_token = 'brandnewtoken'
        config.save()
        config_reload = Config(config_file_path=config_file_path)
        assert_that(path.isfile(config_file_path), is_(True))
        assert_that(config_reload.auth_token, equal_to(config.auth_token))

    @pytest.mark.usefixtures('config_directory', 'default_config_file')
    def test_save_overwrite(self, config_file_path):
        config = Config(config_file_path=config_file_path)
        assert_that(config_file_path, is_not(equal_to('newtoken')))
        config.auth_token = 'newtoken'
        config.save()
        config_reloaded = Config(config_file_path=config_file_path)
        assert_that(config_reloaded.auth_token, equal_to('newtoken'))
