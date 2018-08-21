# # data.world-py
# # Copyright 2017 data.world, Inc.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the
# # License.
# #
# # You may obtain a copy of the License at
# # http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# # implied. See the License for the specific language governing
# # permissions and limitations under the License.
# #
# # This product includes software developed at
# # data.world, Inc.(http://data.world/).
#
# from __future__ import absolute_import
#
# import os
# from os import path
#
# import pytest
# import responses
# from doublex import assert_that, Spy, called, Mock
# from hamcrest import (equal_to, has_entries, has_properties, is_, described_as,
#                       empty, raises, calling, has_key)
#
# from datadotworld import client
#
# from datadotworld.client._swagger.rest import ApiException
# from datadotworld.client._swagger.models import (
#     DatasetSummaryResponse,
#     FileBatchUpdateRequest,
#     FileCreateOrUpdateRequest,
#     FileSourceCreateOrUpdateRequest,
#     PaginatedDatasetResults,
#     UserDataResponse,
#     ProjectSummaryResponse,
#     InsightSummaryResponse,
#     PaginatedProjectResults
# )
# from datadotworld.client.api import RestApiClient, RestApiError
#
#
# class TestApiClient:
#     @pytest.fixture()
#     def datasets_api(self):
#         with Spy(DatasetsApi) as api:
#             api.get_dataset = lambda o, d: DatasetSummaryResponse(
#                                 owner=o,
#                                 id=d,
#                                 title='Dataset',
#                                 visibility='PRIVATE',
#                                 status='LOADED',
#                                 created='2018-02-01T01:03:26.879Z',
#                                 updated='2018-02-01T01:03:28.211Z',
#                                 access_level='ADMIN',
#                                 is_project=False)
#             api.create_dataset_with_http_info = lambda o, b, **kwargs: (
#                 {}, 200, {'Location': 'https://data.world/agentid/datasetid'})
#             return api
#
#     @pytest.fixture()
#     def uploads_api(self):
#         with Spy(UploadsApi) as api:
#             return api
#
#     @pytest.fixture()
#     def download_api(self):
#         with Spy(DownloadApi) as api:
#             api.download_dataset
#             api.download_file
#             return api
#
#     @pytest.fixture()
#     def query_resp(self):
#         with Mock() as response:
#             response.data = 'result'.encode()
#             return response
#
#     @pytest.fixture()
#     def sql_api(self, query_resp):
#         with Spy(SqlApi) as api:
#             api.sql_post = \
#                 lambda o, d, q, sql_api_mock, _preload_content: query_resp
#             return api
#
#     @pytest.fixture()
#     def sparql_api(self, query_resp):
#         with Spy(SparqlApi) as api:
#             api.sparql_post = \
#                 lambda o, d, q, sparql_api_mock, _preload_content: query_resp
#             return api
#
#     @pytest.fixture()
#     def user_api(self):
#         with Spy(UserApi) as api:
#             api.get_user_data = lambda: UserDataResponse(
#                                     id='test',
#                                     created='2018-02-01T01:03:26.879Z',
#                                     updated='2018-02-01T01:03:28.211Z')
#             api.fetch_liked_datasets = lambda: PaginatedDatasetResults(
#                                             count=1,
#                                             records=[])
#             api.fetch_datasets = lambda: PaginatedDatasetResults(count=1,
#                                                                  records=[])
#             api.fetch_contributing_datasets = lambda: PaginatedDatasetResults(
#                                                 count=1,
#                                                 records=[])
#             api.fetch_contributing_projects = lambda: PaginatedProjectResults(
#                                                 count=1,
#                                                 records=[])
#             api.fetch_liked_projects = lambda: PaginatedProjectResults(
#                                             count=1,
#                                             records=[])
#             api.fetch_projects = lambda: PaginatedProjectResults(count=1,
#                                                                  records=[])
#             return api
#
#     @pytest.fixture()
#     def streams_api(self):
#         with Spy(StreamsApi) as api:
#             api.append_records
#             return api
#
#     @pytest.fixture()
#     def projects_api(self):
#         with Spy(ProjectsApi) as api:
#             api.get_project = lambda o, d: ProjectSummaryResponse(
#                                 owner=o,
#                                 id=d,
#                                 title='Project',
#                                 visibility='PRIVATE',
#                                 status='LOADED',
#                                 created='2018-02-01T01:03:26.879Z',
#                                 updated='2018-02-01T01:03:28.211Z',
#                                 access_level='ADMIN')
#             api.create_project = lambda o, **kwargs: (
#                 {}, 200, {'Location': 'https://data.world/agentid/projectid'})
#             return api
#
#     @pytest.fixture()
#     def insights_api(self):
#         with Spy(InsightsApi) as api:
#             api.get_insight = lambda o, d, i: InsightSummaryResponse(
#                                 id=i,
#                                 title='Insights',
#                                 body={},
#                                 author=o,
#                                 created='2018-02-01T01:03:26.879Z',
#                                 updated='2018-02-01T01:03:28.211Z')
#             api.create_insight_with_http_info = lambda o, d, **kwargs: (
#                 {}, 200, {'Location': 'https://data.world/agentid/projectid'})
#             return api
#
#     @pytest.fixture()
#     def api_client(self, config, datasets_api, uploads_api, download_api,
#                    sql_api, sparql_api, user_api, streams_api, projects_api,
#                    insights_api):
#         client = RestApiClient(config)
#         client._datasets_api = datasets_api
#         client._uploads_api = uploads_api
#         client._download_api = download_api
#         client._sql_api = sql_api
#         client._sparql_api = sparql_api
#         client._user_api = user_api
#         client._streams_api = streams_api
#         client._projects_api = projects_api
#         client._insights_api = insights_api
#         return client
#
#     def test_get_dataset(self, api_client, dataset_key):
#         dataset = api_client.get_dataset(dataset_key)
#         assert_that(dataset, has_entries(
#             {'owner': equal_to('agentid'), 'id': equal_to('datasetid')}))
#
#     def test_create_dataset(self, api_client):
#         create_request = {'title': 'Dataset', 'visibility': 'OPEN',
#                           'license': 'Public Domain'}
#         dataset_key = api_client.create_dataset('agentid', **create_request)
#         assert_that(dataset_key,
#                     equal_to('https://data.world/agentid/datasetid'))
#
#     def test_update_dataset(self, api_client, datasets_api, dataset_key):
#         patch_request = {'tags': ['tag1', 'tag2']}
#         api_client.update_dataset(dataset_key, **patch_request)
#         assert_that(datasets_api.patch_dataset,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('datasetid'),
#                                                 has_properties(patch_request)))
#
#     def test_replace_dataset(self, api_client, datasets_api, dataset_key):
#         replace_request = {'title': 'Dataset', 'visibility': 'OPEN'}
#         api_client.replace_dataset(dataset_key, **replace_request)
#         assert_that(datasets_api.replace_dataset,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('datasetid'),
#                                                 has_properties(
#                                                     replace_request)))
#
#     def test_delete_dataset(self, api_client, datasets_api, dataset_key):
#         api_client.delete_dataset(dataset_key)
#         assert_that(datasets_api.delete_dataset,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('datasetid')))
#
#     def test_add_files_via_url(self, api_client, datasets_api, dataset_key):
#         file_update_request = {'filename.ext':
#                                {'url': 'https://acme.inc/filename.ext'}}
#         file_update_object = FileBatchUpdateRequest(
#             files=[FileCreateOrUpdateRequest(
#                 name='filename.ext',
#                 source=FileSourceCreateOrUpdateRequest(
#                     url='https://acme.inc/filename.ext'))])
#
#         api_client.add_files_via_url(dataset_key, file_update_request)
#         assert_that(datasets_api.add_files_by_source,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('datasetid'),
#                                                 equal_to(file_update_object)))
#
#     def test_sync_files(self, api_client, datasets_api, dataset_key):
#         api_client.sync_files(dataset_key)
#         assert_that(datasets_api.sync,
#                     called().times(1).with_args('agentid', 'datasetid'))
#
#     def test_upload_files(self, api_client, uploads_api, dataset_key):
#         files = ['filename.ext']
#         api_client.upload_files(dataset_key, files)
#         assert_that(uploads_api.upload_files,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('datasetid'),
#                                                 equal_to(files)))
#
#     def test_upload_file(self, api_client, uploads_api, dataset_key):
#         name = 'filename.ext'
#         api_client.upload_file(dataset_key, name)
#         assert_that(uploads_api.upload_file,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('datasetid'),
#                                                 equal_to(name)))
#
#     def test_delete_files(self, api_client, datasets_api, dataset_key):
#         files = ['filename.ext']
#         api_client.delete_files(dataset_key, files)
#         assert_that(datasets_api.delete_files_and_sync_sources,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('datasetid'),
#                                                 equal_to(files)))
#
#     def test_rest_api_error(self):
#         apix = ApiException(status=400, reason="boom")
#         e = RestApiError(cause=apix)
#         assert_that(e.status, equal_to(400))
#         assert_that(e.reason, equal_to("boom"))
#         assert_that(e.body, equal_to(None))
#         assert_that(e.cause, equal_to(apix))
#
#     # TODO Test CRUD exception cases
#
#     def test_download_datapackage(self, helpers, config,
#                                   test_datapackages_path, api_client,
#                                   dataset_key):
#         datapackage_zip = path.join(test_datapackages_path,
#                                     'the-simpsons-by-the-data.zip')
#         with responses.RequestsMock() as rsps, open(datapackage_zip,
#                                                     'rb') as file:
#             @helpers.validate_request_headers()
#             def datapackage_endpoint(_):
#                 return 200, {}, file.read()
#
#             rsps.add_callback(
#                 rsps.GET,
#                 'https://download.data.world/datapackage/agentid/datasetid',
#                 datapackage_endpoint)
#
#             datapackage = api_client.download_datapackage(dataset_key,
#                                                           config.cache_dir)
#
#             assert_that(datapackage, equal_to(
#                 path.join(config.cache_dir, 'datapackage.json')))
#             assert_that(path.isfile(datapackage),
#                         described_as('%0 is a file', is_(True), datapackage))
#
#             data_subdirectory = path.join(config.cache_dir, 'data')
#             assert_that(path.isdir(data_subdirectory),
#                         described_as('%0 is a directory', is_(True),
#                                      data_subdirectory))
#             assert_that(os.listdir(config.tmp_dir),
#                         described_as('%0 is empty', empty(), config.tmp_dir))
#
#     def test_download_datapackage_error(self, helpers, config,
#                                         test_datapackages_path, api_client,
#                                         dataset_key):
#         datapackage_zip = path.join(test_datapackages_path,
#                                     'the-simpsons-by-the-data.zip')
#         with responses.RequestsMock() as rsps, open(datapackage_zip,
#                                                     'rb') as file:  # noqa
#             @helpers.validate_request_headers()
#             def datapackage_endpoint(_):
#                 return 400, {}, ''
#
#             rsps.add_callback(
#                 rsps.GET,
#                 'https://download.data.world/datapackage/agentid/datasetid',
#                 datapackage_endpoint)
#
#             assert_that(
#                 calling(api_client.download_datapackage).with_args(
#                     dataset_key, config.cache_dir),
#                 raises(RestApiError))
#
#     def test_download_datapackage_existing_dest_dir(
#             self, config, api_client, dataset_key):
#         os.mkdir(config.cache_dir)
#         assert_that(
#             calling(api_client.download_datapackage).with_args(
#                 dataset_key, config.cache_dir),
#             raises(ValueError))
#
#     def test_download_dataset(self, api_client, dataset_key, download_api):
#         api_client.download_dataset(dataset_key)
#         assert_that(download_api.download_dataset,
#                     called().times(1).with_args('agentid', 'datasetid'))
#
#     def test_download_file(self, api_client, dataset_key, download_api):
#         api_client.download_file(dataset_key, 'file')
#         assert_that(download_api.download_file,
#                     called().times(1).with_args('agentid', 'datasetid',
#                                                 'file'))
#
#     def test_sql(self, api_client, dataset_key, sql_api):
#         result = api_client.sql(dataset_key, 'query', sql_api_mock=sql_api)
#         assert_that(result.read().decode('utf-8'), equal_to('result'))
#
#     def test_sparql(self, api_client, dataset_key, sparql_api):
#         result = api_client.sparql(dataset_key, 'query',
#                                    sparql_api_mock=sparql_api)
#         assert_that(result.read().decode('utf-8'), equal_to('result'))
#
#     def test_get_user_data(self, api_client):
#         user_data_response = api_client.get_user_data()
#         assert_that(user_data_response,
#                     has_key(equal_to('display_name')))
#
#     def test_fetch_liked_datasets(self, api_client, user_api):
#         liked_datasets = api_client.fetch_liked_datasets()
#         assert_that(user_api.fetch_liked_datasets(),
#                     has_properties(liked_datasets))
#
#     def test_fetch_contributing_datasets(self, api_client, user_api):
#         contributing_datasets = api_client.fetch_contributing_datasets()
#         assert_that(user_api.fetch_contributing_datasets(),
#                     has_properties(contributing_datasets))
#
#     def test_fetch_datasets(self, api_client, user_api):
#         user_datasets = api_client.fetch_datasets()
#         assert_that(user_api.fetch_datasets(),
#                     has_properties(user_datasets))
#
#     def test_fetch_contributing_projects(self, api_client, user_api):
#         contributing_projects = api_client.fetch_contributing_projects()
#         assert_that(user_api.fetch_contributing_projects(),
#                     has_properties(contributing_projects))
#
#     def test_fetch_liked_projects(self, api_client, user_api):
#         liked_projects = api_client.fetch_liked_projects()
#         assert_that(user_api.fetch_liked_projects(),
#                     has_properties(liked_projects))
#
#     def test_fetch_projects(self, api_client, user_api):
#         projects = api_client.fetch_projects()
#         assert_that(user_api.fetch_projects(), has_properties(projects))
#
#     def test_append_records(self, api_client, dataset_key, streams_api):
#         body = {'content': 'content'}
#         api_client.append_records(dataset_key, 'streamid', body)
#         assert_that(streams_api.append_records,
#                     called().times(1).with_args('agentid', 'datasetid',
#                                                 'streamid', body))
#
#     def test_get_project(self, api_client, project_key):
#         project = api_client.projects.get_project(project_key)
#         assert_that(project, has_entries(
#             {'owner': equal_to('agentid'), 'id': equal_to('projectid')}))
#
#     def test_create_project(self, api_client):
#         create_request = {'title': 'Project', 'visibility': 'OPEN'}
#         project_key = api_client.create_project('agentid', **create_request)
#         assert_that(project_key,
#                     equal_to('https://data.world/agentid/projectid'))
#
#     def test_update_project(self, api_client, projects_api, project_key):
#         update_request = {'tags': ['tag1', 'tag2']}
#         api_client.update_project(project_key, **update_request)
#         assert_that(projects_api.patch_project,
#                     called().times(1))
#
#     def test_replace_project(self, api_client, projects_api, project_key):
#         replace_request = {'title': 'New Project', 'visibility': 'OPEN'}
#         api_client.replace_project(project_key, **replace_request)
#         assert_that(projects_api.replace_project,
#                     called().times(1))
#
#     def test_add_linked_dataset(self, api_client, projects_api, project_key,
#                                 dataset_key):
#         api_client.add_linked_dataset(project_key, dataset_key)
#         assert_that(projects_api.add_linked_dataset,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('projectid'),
#                                                 equal_to('agentid'),
#                                                 equal_to('datasetid')))
#
#     def test_remove_linked_dataset(self, api_client, projects_api, project_key,
#                                    dataset_key):
#         api_client.remove_linked_dataset(project_key, dataset_key)
#         assert_that(projects_api.remove_linked_dataset,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('projectid'),
#                                                 equal_to('agentid'),
#                                                 equal_to('datasetid')))
#
#     def test_delete_project(self, api_client, projects_api, project_key):
#         api_client.delete_project(project_key)
#         assert_that(projects_api.delete_project,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('projectid')))
#
#     def test_get_insight(self, api_client, project_key,
#                          insight_id='insightid'):
#         insight = api_client.get_insight(project_key, insight_id)
#         assert_that(insight, has_entries(
#             {'author': equal_to('agentid'), 'id': equal_to(insight_id)}))
#
#     def test_get_insight_for_project(self, api_client, insights_api,
#                                      project_key):
#         api_client.get_insights_for_project(project_key)
#         assert_that(insights_api.get_insights_for_project,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('projectid')))
#
#     def test_create_insight(self, api_client, project_key):
#         create_request = {'title': 'Insight', 'image_url': 'https://image.url'}
#         new_insight = api_client.create_insight(project_key,
#                                                 **create_request)
#         assert_that(new_insight,
#                     equal_to('https://data.world/agentid/projectid'))
#
#     def test_replace_insight(self, api_client, insights_api, project_key,
#                              insight_id='insightid'):
#         replace_request = {'title': 'Replace Insight',
#                            'image_url': 'https://image.com/'}
#         api_client.replace_insight(project_key, insight_id,
#                                    **replace_request)
#         assert_that(insights_api.replace_insight,
#                     called().times(1))
#
#     def test_update_insight(self, api_client, insights_api, project_key,
#                             insight_id='insightid'):
#         patch_request = {'title': 'patch insight'}
#         api_client.update_insight(project_key, insight_id, **patch_request)
#         assert_that(insights_api.update_insight,
#                     called().times(1))
#
#     def test_delete_insight(self, api_client, insights_api, project_key,
#                             insight_id='insightid'):
#         api_client.delete_insight(project_key, insight_id)
#         assert_that(insights_api.delete_insight,
#                     called().times(1).with_args(equal_to('agentid'),
#                                                 equal_to('projectid'),
#                                                 equal_to(insight_id)))
