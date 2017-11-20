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

import configparser
import os
import re
import tempfile
from os import path

import six


class DefaultConfig(object):
    """Base class for configuration objects

    This class defines default values and establishes the contract for
    sub-classes.

    Attributes
    ----------
    auth_token : str
        API token for access to data.world.
    tmp_dir : str
        Path of temporary directory, where temporary files are created.
    cache_dir : str
        Path of dataset cache directory, where downloaded datasets are saved.
    """

    def __init__(self):
        self._auth_token = None
        self._tmp_dir = path.expanduser(tempfile.gettempdir())
        self._cache_dir = path.expanduser('~/.dw/cache')

    @property
    def auth_token(self):
        return self._auth_token

    @property
    def cache_dir(self):
        return self._cache_dir

    @property
    def tmp_dir(self):
        return self._tmp_dir


class EnvConfig(DefaultConfig):
    """Environment-based configuration

    This class will obtain configuration parameters from environment variables:
    - DW_AUTH_TOKEN
    - DW_CACHE_DIR
    - DW_TMP_DIR
    """

    def __init__(self):
        super(EnvConfig, self).__init__()
        self._auth_token = os.environ.get('DW_AUTH_TOKEN')
        self._cache_dir = os.environ.get('DW_CACHE_DIR')
        self._tmp_dir = os.environ.get('DW_TMP_DIR')


class FileConfig(DefaultConfig):
    """File-based configuration

    This class allows configuration to be saved to and obtained from
    data.world's configuration file.

    Multiple configurations profiles can be saved in the same file and are
    identified by their profile name.

    :param profile: Name of configuration profile.
    :type profile: str
    """

    def __init__(self, profile='default', **kwargs):
        super(FileConfig, self).__init__()

        # Overrides, for testing
        self._config_file_path = path.expanduser(
            kwargs.get('config_file_path', '~/.dw/config'))
        legacy_file_path = path.expanduser(
            kwargs.get('legacy_file_path', '~/.data.world'))

        if not path.isdir(path.dirname(self._config_file_path)):
            os.makedirs(path.dirname(self._config_file_path))

        self._config_parser = (configparser.ConfigParser()
                               if six.PY3 else configparser.SafeConfigParser())

        if path.isfile(self._config_file_path):
            self._config_parser.read_file(open(self._config_file_path))
            if self.__migrate_invalid_defaults(self._config_parser) > 0:
                self.save()
        elif path.isfile(legacy_file_path):
            self._config_parser = self.__migrate_config(legacy_file_path)
            self.save()

        self._profile = profile
        self._section = (profile
                         if profile.lower() != configparser.DEFAULTSECT.lower()
                         else configparser.DEFAULTSECT)

        if not path.isdir(path.dirname(self.cache_dir)):
            os.makedirs(path.dirname(self.cache_dir))

    @property
    def auth_token(self):
        self.__validate_config()
        return self._config_parser.get(self._section, 'auth_token')

    @auth_token.setter
    def auth_token(self, auth_token):
        """

        :param auth_token:

        """
        if (self._section != configparser.DEFAULTSECT and
                not self._config_parser.has_section(self._section)):
            self._config_parser.add_section(self._section)
        self._config_parser.set(self._section, 'auth_token', auth_token)

    def save(self):
        """Persist config changes"""
        with open(self._config_file_path, 'w') as file:
            self._config_parser.write(file)

    def __validate_config(self):
        if not path.isfile(self._config_file_path):
            raise RuntimeError(
                'Configuration file not found at {}.'
                'To fix this issue, run dw configure'.format(
                    self._config_file_path))
        if not self._config_parser.has_option(self._section, 'auth_token'):
            raise RuntimeError(
                'The {0} profile is not properly configured. '
                'To fix this issue, run dw -p {0} configure'.format(
                    self._profile))

    @staticmethod
    def __migrate_config(legacy_file_path):
        config_parser = configparser.ConfigParser()

        with open(legacy_file_path, 'r') as legacy:
            regex = re.compile(r"^token\s*=\s*(\S.*)$")
            token = next(iter(
                [regex.match(line.strip()).group(1) for line in legacy if
                 regex.match(line)]),
                None)
            if token is not None:
                config_parser[configparser.DEFAULTSECT] = {'auth_token': token}

        # Will leave legacy in case R SDK may still need it
        # os.remove(legacy_file_path)

        return config_parser

    @staticmethod
    def __migrate_invalid_defaults(config_parser):
        # This fixes an issue related to us having referred to the default
        # section in the config file as 'default' as opposed to using
        # configparser.DEFAULTSECT
        # That may result in 'ValueError: Invalid section name: default'
        # https://github.com/datadotworld/data.world-py/issues/18
        invalid_defaults = []
        for section in config_parser.sections():
            # Doesn't include DEFAULTSECT, but checking nonetheless
            if (section != configparser.DEFAULTSECT and
                    section.lower() == configparser.DEFAULTSECT.lower()):
                invalid_defaults.append(section)

        if len(invalid_defaults) == 1:
            old_default = invalid_defaults[0]
            config_parser[configparser.DEFAULTSECT] = {
                option: config_parser.get(old_default, option)
                for option in config_parser.options(old_default)}

        for section in invalid_defaults:
            config_parser.remove_section(section)

        return len(invalid_defaults)


class ChainedConfig(DefaultConfig):
    """Checks for env config first, then file-based config"""

    def __init__(self, **kwargs):
        # Overrides (for testing)
        self._config_chain = kwargs.get('config_chain',
                                        [EnvConfig(), FileConfig()])

    def __getattribute__(self, item):
        """Delegates requests to config objects in the chain
        """
        return object.__getattribute__(self, '_first_not_none')(
            object.__getattribute__(self, '_config_chain'),
            lambda c: c.__getattribute__(item))

    @staticmethod
    def _first_not_none(seq, supplier_func):
        """Applies supplier_func to each element in seq, returns 1st not None

        :param seq: Sequence of object
        :type seq: iterable
        :param supplier_func: Function that extracts the desired value from
            elements in seq
        :type supplier_func: function
        """
        for i in seq:
            obj = supplier_func(i)
            if obj is not None:
                return obj

        return None


class InlineConfig(DefaultConfig):
    def __init__(self, token):
        super(InlineConfig, self).__init__()
        self._auth_token = token
