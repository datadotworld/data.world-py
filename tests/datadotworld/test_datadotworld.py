import pytest
import responses
from doublex import Stub, assert_that
from hamcrest import has_entry, equal_to, calling, raises

from datadotworld import DataDotWorld
from datadotworld.config import Config


class TestDataDotWorld:
    @pytest.fixture
    def dw(self):
        with Stub(Config) as config:
            config.auth_token = 'token'
        return DataDotWorld(config=config)

    @pytest.fixture
    def sql_endpoint(self):
        return 'https://query.data.world/sql/owner/dataset'

    @pytest.fixture
    def sql_query(self):
        return 'SELECT * FROM beans'

    @pytest.fixture
    def beans_csv(self):
        return 'cool,beans\n1,2\n3,4'

    @pytest.fixture
    def success_response(self, beans_csv):
        return 200, {}, beans_csv

    def test_query(self, dw, sql_endpoint, sql_query, success_response, beans_csv):
        with responses.RequestsMock() as rsps:
            rsps.add_callback(rsps.GET, '{}?query={}'.format(sql_endpoint, sql_query), content_type='text/csv',
                              callback=lambda req: verify_auth(req, success_response), match_querystring=True)

            result = dw.query('owner/dataset', sql_query)
            assert_that(result.raw, equal_to(beans_csv))

    def test_query_400(self, dw, sql_endpoint, sql_query):
        with responses.RequestsMock() as rsps:
            rsps.add(rsps.GET, '{}?query={}'.format(sql_endpoint, sql_query), match_querystring=True, status=400)

            assert_that(calling(dw.query).with_args('owner/dataset', sql_query), raises(RuntimeError))


def verify_auth(request, response):
    assert_that(request.headers, has_entry('Authorization', equal_to('Bearer token')))
    return response
