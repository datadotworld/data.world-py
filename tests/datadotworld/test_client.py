import pytest
import requests

from datadotworld import DataDotWorld, __version__
from datadotworld.models import *


class TestDataDotWorld:
    @pytest.fixture
    def dw(self):
        return DataDotWorld('mytesttoken')

    def test_get_dataset(self, dw, monkeypatch):
        monkeypatch.setattr(dw._datasets_api, 'get_dataset', lambda o, d: DatasetSummaryResponse(o, d))
        dataset = dw.get_dataset('agentid/datasetid')
        assert dataset.owner == 'agentid'
        assert dataset.id == 'datasetid'

    def test_create_dataset(self, dw, monkeypatch):
        create_request = DatasetCreateRequest(title='Dataset', visibility='OPEN')

        def create_function(owner_id, body):
            assert owner_id == 'agentid'
            assert body == create_request

        monkeypatch.setattr(dw._datasets_api, 'create_dataset', create_function)

        dw.create_dataset('agentid', create_request)

    def test_patch_dataset(self, dw, monkeypatch):
        patch_request = DatasetPatchRequest()

        def patch_function(owner_id, dataset_id, body):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert body == patch_request

        monkeypatch.setattr(dw._datasets_api, 'patch_dataset', patch_function)

        dw.patch_dataset('agentid/datasetid', patch_request)

    def test_replace_dataset(self, dw, monkeypatch):
        replace_request = DatasetPutRequest(visibility='OPEN')

        def replace_function(owner_id, dataset_id, body):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert body == replace_request

        monkeypatch.setattr(dw._datasets_api, 'replace_dataset', replace_function)

        dw.replace_dataset('agentid/datasetid', replace_request)

    def test_add_files_via_url(self, dw, monkeypatch):
        file_update_request = FileBatchUpdateRequest(files=[
            FileCreateOrUpdateRequest(name='filename.ext',
                                      source=FileSourceCreateOrUpdateRequest(url='https://acme.inc/filename.ext'))
        ])

        def add_files_function(owner_id, dataset_id, body):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert body == file_update_request

        monkeypatch.setattr(dw._datasets_api, 'add_files_by_source', add_files_function)

        dw.add_files_via_url("agentid/datasetid", file_update_request)

    def test_sync_files(self, dw, monkeypatch):
        def sync_function(owner_id, dataset_id):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'

        monkeypatch.setattr(dw._datasets_api, 'sync', sync_function)

        dw.sync_files("agentid/datasetid")

    def test_upload_files(self, dw, monkeypatch):
        def upload_function(owner_id, dataset_id, file):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert file == ['filename.ext']

        monkeypatch.setattr(dw._uploads_api, 'upload_files', upload_function)

        dw.upload_files('agentid/datasetid', ['filename.ext'])

    def test_delete_files(self, dw, monkeypatch):
        def delete_function(owner_id, dataset_id, names):
            assert owner_id == 'agentid'
            assert dataset_id == 'datasetid'
            assert names == ['filename.ext']

        monkeypatch.setattr(dw._datasets_api, 'delete_files_and_sync_sources', delete_function)

        dw.delete_files('agentid/datasetid', ['filename.ext'])

    def test_query_sql(self, dw, monkeypatch):
        expected_url = '{0.protocol}://{0.query_host}/sql/agentid/datasetid'.format(dw)
        expected_params = {'query': 'SELECT * FROM Tables'}
        expected_headers = {
            'User-Agent': 'data.world-py - {0}'.format(__version__),
            'Accept': 'text/csv',
            'Authorization': 'Bearer {0}'.format(dw.token)
        }
        response = requests.Response()
        response.status_code = 200
        monkeypatch.setattr(requests, 'get', requests_get_stub(expected_url, expected_params, expected_headers,
                                                               response))

        results = dw.query('agentid/datasetid', 'SELECT * FROM Tables')

        assert results.as_string() == ''

    # TODO Add test scenarios for query


def requests_get_stub(expected_url, expected_params, expected_headers, response):
    def query_function(url, params=None, headers=None):
        assert url == expected_url
        assert params == expected_params
        assert headers == expected_headers
        return response

    return query_function
