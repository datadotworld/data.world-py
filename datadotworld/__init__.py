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

from datadotworld.datadotworld import DataDotWorld

__version__ = '0.1.2'


def load_dataset(dataset_key, profile='default'):
    return DataDotWorld(profile=profile).load_dataset(dataset_key)


def query(dataset_key, query, query_type='sql', profile='default'):
    return DataDotWorld(profile=profile).query(dataset_key, query, query_type=query_type)


def api_client(profile='default'):
    return DataDotWorld(profile=profile).api_client
