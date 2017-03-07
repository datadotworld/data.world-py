import pytest

from datadotworld.client.api import ApiClient
from datadotworld.client._swagger.models import *


class TestApiClient:
    @pytest.fixture
    def api_client(self):
        return ApiClient()

    def test_get_dataset(self, api_client, monkeypatch):
        monkeypatch.setattr(api_client._datasets_api, 'get_dataset', lambda o, d: DatasetSummaryResponse(o, d))
        dataset = api_client.get_dataset('agentid/datasetid')
        assert dataset['owner'] == 'agentid'
        assert dataset['id'] == 'datasetid'

    def test_create_dataset(self, api_client, monkeypatch):
        create_request = {'title': 'Dataset', 'visibility': 'OPEN', 'license': 'Public Domain'}

        create_calls = Counter()

        def create_function(owner_id, body):
            assert owner_id == 'agentid'
            assert body.title == create_request['title']
            assert body.visibility == create_request['visibility']
            assert body.license == create_request['license']

            create_calls.inc()

        monkeypatch.setattr(api_client._datasets_api, 'create_dataset', create_function)

        api_client.create_dataset('agentid', **create_request)

        assert create_calls.count == 1

    def test_patch_dataset(self, api_client, monkeypatch):
        patch_request = {'tags': ['tag1', 'tag2']}

        patch_calls = Counter()

        def patch_function(owner_id, dataset_id, body):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert body.tags == patch_request['tags']

            patch_calls.inc()

        monkeypatch.setattr(api_client._datasets_api, 'patch_dataset', patch_function)

        api_client.patch_dataset('agentid/datasetid', **patch_request)

        assert patch_calls.count == 1

    def test_replace_dataset(self, api_client, monkeypatch):
        replace_request = {'visibility': 'OPEN'}

        replace_calls = Counter()

        def replace_function(owner_id, dataset_id, body):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert body.visibility == replace_request['visibility']

            replace_calls.inc()

        monkeypatch.setattr(api_client._datasets_api, 'replace_dataset', replace_function)

        api_client.replace_dataset('agentid/datasetid', **replace_request)

        assert replace_calls.count == 1

    def test_add_files_via_url(self, api_client, monkeypatch):
        file_update_request = {'filename.ext': 'https://acme.inc/filename.ext'}

        add_files_calls = Counter()

        def add_files_function(owner_id, dataset_id, body):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert body.files[0].name == 'filename.ext'
            assert body.files[0].source.url == 'https://acme.inc/filename.ext'
            assert len(body.files) == 1

            add_files_calls.inc()

        monkeypatch.setattr(api_client._datasets_api, 'add_files_by_source', add_files_function)

        api_client.add_files_via_url("agentid/datasetid", file_update_request)

        assert add_files_calls.count == 1

    def test_sync_files(self, api_client, monkeypatch):
        sync_calls = Counter()

        def sync_function(owner_id, dataset_id):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'

            sync_calls.inc()

        monkeypatch.setattr(api_client._datasets_api, 'sync', sync_function)

        api_client.sync_files("agentid/datasetid")

        assert sync_calls.count == 1

    def test_upload_files(self, api_client, monkeypatch):
        upload_calls = Counter()

        def upload_function(owner_id, dataset_id, file):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert file == ['filename.ext']

            upload_calls.inc()

        monkeypatch.setattr(api_client._uploads_api, 'upload_files', upload_function)

        api_client.upload_files('agentid/datasetid', ['filename.ext'])

        assert upload_calls.count == 1

    def test_delete_files(self, api_client, monkeypatch):
        delete_calls = Counter()

        def delete_function(owner_id, dataset_id, names):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert names == ['filename.ext']

            delete_calls.inc()

        monkeypatch.setattr(api_client._datasets_api, 'delete_files_and_sync_sources', delete_function)

        api_client.delete_files('agentid/datasetid', ['filename.ext'])

        assert delete_calls.count == 1

        # def test_query_sql(self, dw, monkeypatch):
        #     expected_url = '{0.protocol}://{0.query_host}/sql/agentid/datasetid'.format(dw)
        #     expected_params = {'query': 'SELECT * FROM Tables'}
        #     expected_headers = {
        #         'User-Agent': 'data.world-py - {0}'.format(__version__),
        #         'Accept': 'text/csv',
        #         'Authorization': 'Bearer {0}'.format(api_client.token)
        #     }
        #     response = requests.Response()
        #     response.status_code = 200
        #     monkeypatch.setattr(requests, 'get', requests_get_stub(expected_url, expected_params, expected_headers,
        #                                                            response))
        #
        #     results = dw.query('agentid/datasetid', 'SELECT * FROM Tables')
        #
        #     assert results.as_string() == ''
        #
        # # TODO Add test scenarios for query
        #
        #
        # def requests_get_stub(expected_url, expected_params, expected_headers, response):
        #     def query_function(url, params=None, headers=None):
        #         assert url == expected_url
        #         assert params == expected_params
        #         assert headers == expected_headers
        #         return response
        #
        #     return query_function


class Counter:
    def __init__(self):
        self.count = 0

    def inc(self):
        self.count += 1