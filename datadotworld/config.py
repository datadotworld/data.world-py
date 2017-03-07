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
import configparser
import re

from os import path


class Config:
    def __init__(self, profile='default', **kwargs):
        config_file_path = kwargs.get('config_file_path') or path.expanduser('~/.datadotworld')
        legacy_file_path = kwargs.get('legacy_file_path') or path.expanduser('~/.data.world')

        if path.isfile(config_file_path):
            config_parser = configparser.ConfigParser()
            config_parser.read_file(open(config_file_path))
        elif path.isfile(legacy_file_path):
            config_parser = self.__migrate_config(legacy_file_path, config_file_path)
        else:
            raise RuntimeError('Unable to locate configuration file {}. '
                               'To fix this issue, run dw configure'.format(config_file_path))

        self._config_file_path = config_file_path
        self._config_parser = config_parser
        self._profile = profile

    @property
    def auth_token(self):
        if self._profile not in self._config_parser:
            return None
        return self._config_parser[self._profile].get('auth_token')

    @auth_token.setter
    def auth_token(self, auth_token):
        if self._profile not in self._config_parser:
            self._config_parser[self._profile] = {}
        self._config_parser[self._profile]['auth_token'] = auth_token

    def save(self):
        self._config_parser.write(open(self._config_file_path, 'w'))

    @staticmethod
    def __migrate_config(legacy_file_path, target_file_path):
        config_parser = configparser.ConfigParser()
        with open(legacy_file_path, 'r') as legacy, open(target_file_path, 'w') as target:
            regex = re.compile(r"^token\s*=\s*(\S.*)$")
            token = next(iter([regex.match(line.strip()).group(1) for line in legacy if regex.match(line)]),
                              None)
            config_parser['default'] = {'auth_token': token}
            config_parser.write(target)
        return config_parser


