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

# This product includes software developed at
# data.world, Inc.(http://data.world/).

from __future__ import absolute_import

import os
from os import path

import pytest
import responses
from doublex import assert_that, Spy, called, Mock
from hamcrest import (equal_to, has_entries, has_properties, is_, described_as,
                      empty, raises, calling, has_key)

from datadotworld import client
from datadotworld.client.api_client import ApiClient
from datadotworld.client.api import RestApiClient, RestApiError
from datadotworld.client.projects_api import ProjectsApi


class TestApiClient:
    @pytest.fixture()
    def projects_api(self):
        with Spy(ProjectsApi) as api:
            api.get_project = lambda o, d: ProjectSummaryResponse(
                                owner=o,
                                id=d,
                                title='Project',
                                visibility='PRIVATE',
                                status='LOADED',
                                created='2018-02-01T01:03:26.879Z',
                                updated='2018-02-01T01:03:28.211Z',
                                access_level='ADMIN')
            api.create_project = lambda o, **kwargs: (
                {}, 200, {'Location': 'https://data.world/agentid/projectid'})
            return api

    @pytest.fixture()
    def api_client(self, api_token='just_a_test_token'):
        client = ApiClient(api_token)
        return client

    def test_get_project(self, api_client, owner_id='agentid', project_id='projectid'):
        project = api_client.projects.get_project(owner_id, project_id)
        assert_that(project, has_entries(
            {'owner': equal_to('agentid'), 'id': equal_to('projectid')}))

    def test_create_project(self, api_client):
        create_request = {'title': 'Project', 'visibility': 'OPEN'}
        project_key = api_client.projects.create_project('agentid', **create_request)
        assert_that(project_key,
                    equal_to('https://data.world/agentid/projectid'))

    def test_update_project(self, api_client, projects_api, owner_id='agentid', project_id='projectid'):
        update_request = {'tags': ['tag1', 'tag2']}
        api_client.projects.patch_project(owner_id, project_id, **update_request)
        assert_that(projects_api.patch_project,
                    called().times(1))

    def test_replace_project(self, api_client, projects_api, owner_id='agentid', project_id='projectid'):
        replace_request = {'title': 'New Project', 'visibility': 'OPEN'}
        api_client.projects.replace_project(owner_id, project_id, **replace_request)
        assert_that(projects_api.replace_project,
                    called().times(1))

    def test_add_linked_dataset(self, api_client, projects_api, owner_id='agentid', project_id='projectid',
                                   linked_dataset_owner='agentid', linked_dataset_id='projectid'):
        api_client.projects.add_linked_dataset(owner_id, project_id, linked_dataset_owner, linked_dataset_id)
        assert_that(projects_api.add_linked_dataset,
                    called().times(1).with_args(equal_to('agentid'),
                                                equal_to('projectid'),
                                                equal_to('agentid'),
                                                equal_to('datasetid')))

    def test_remove_linked_dataset(self, api_client, projects_api, owner_id='agentid', project_id='projectid',
                                   linked_dataset_owner='agentid', linked_dataset_id='projectid'):
        api_client.projects.remove_linked_dataset(owner_id, project_id, linked_dataset_owner, linked_dataset_id)
        assert_that(projects_api.remove_linked_dataset,
                    called().times(1).with_args(equal_to('agentid'),
                                                equal_to('projectid'),
                                                equal_to('agentid'),
                                                equal_to('datasetid')))

    def test_delete_project(self, api_client, projects_api, owner_id='agentid', project_id='projectid'):
        api_client.projects.delete_project(owner_id, project_id)
        assert_that(projects_api.delete_project,
                    called().times(1).with_args(equal_to('agentid'),
                                                equal_to('projectid')))

