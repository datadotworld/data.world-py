import pytest
import responses
from doublex import Stub, assert_that
from hamcrest import has_entry, equal_to, calling, raises

from datadotworld.datadotworld import DataDotWorld
from datadotworld.config import Config


class TestDataDotWorld:
    query_types = [
        # Using proper queries here trips the responses framework when they are url-encoded and causes tests to fail
        ('sparql', 'https://query.data.world/sparql/owner/dataset', 'notreallysparql'),
        ('sql', 'https://query.data.world/sql/owner/dataset', 'notreallysql')
    ]

    @pytest.fixture
    def dw(self):
        with Stub(Config) as config:
            config.auth_token = 'token'
        return DataDotWorld(config=config)

    @pytest.fixture
    def beans_csv(self):
        return 'cool,beans\n1,2\n3,4'

    @pytest.fixture
    def success_response(self, beans_csv):
        return 200, {}, beans_csv

    @pytest.mark.parametrize("type,endpoint,query", query_types, ids=['sparql', 'sql'])
    def test_query(self, dw, type, endpoint, query, success_response, beans_csv):
        with responses.RequestsMock() as rsps:
            rsps.add_callback(rsps.GET, '{}?query={}'.format(endpoint, query), content_type='text/csv',
                              callback=lambda req: verify_auth(req, success_response), match_querystring=True)

            result = dw.query('owner/dataset', query, query_type=type)
            assert_that(result.raw_data, equal_to(beans_csv))

    @pytest.mark.parametrize("type,endpoint,query", query_types, ids=['sparql', 'sql'])
    def test_query_400(self, dw, type, endpoint, query):
        with responses.RequestsMock() as rsps:
            rsps.add(rsps.GET, '{}?query={}'.format(endpoint, query), match_querystring=True,
                     status=400)

            assert_that(calling(dw.query).with_args('owner/dataset', query, query_type=type), raises(RuntimeError))


def verify_auth(request, response):
    assert_that(request.headers, has_entry('Authorization', equal_to('Bearer token')))
    return response
