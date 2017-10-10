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

from __future__ import absolute_import

import json
from os import path

import pytest
from doublex import assert_that
from hamcrest import equal_to, has_length, contains, has_key

from datadotworld.models.query import QueryResults


class TestQueryResults:
    @pytest.fixture(params=['sql_select.json'], ids=lambda x: x.split('.')[0])
    def query_result_example(self, test_queries_path, request):
        with open(path.join(test_queries_path, request.param),
                  'r') as json_results:
            return json.load(json_results)

    @pytest.fixture()
    def query_results(self, query_result_example):
        return QueryResults(query_result_example)

    def test_describe(self, query_result_example, query_results):
        metadata_names = [c['name'] for c in query_result_example['metadata']]
        field_names = [f['name'] for f in query_results.describe()['fields']]
        assert_that(field_names, contains(*metadata_names))

    def test_raw_data(self, query_results, query_result_example):
        assert_that(query_results.raw_data, equal_to(query_result_example))

    def test_table(self, query_result_example, query_results):
        metadata_names = [c['name'] for c in query_result_example['metadata']]
        for row in query_results.table:
            assert_that(row.keys(), contains(*metadata_names))
            assert_that(row.values(),
                        contains(*(row[f] for f in metadata_names)))
        assert_that(query_results.table,
                    has_length(
                        len(query_result_example['results']['bindings'])))

    @pytest.mark.parametrize('query_result_example', [
        'sparql_ask.json',
        'sparql_construct.json',
        'sparql_construct_mixed_types.json',
        'sparql_describe.json',
        'sparql_select.json',
        'sparql_select_hof.json',
        'sql_select.json',
        'sql_select2.json',
        'sql_select_empty.json'
    ], indirect=True, ids=lambda x: x.split('.')[0])
    def test_table_parameterized(self, query_result_example, query_results):
        if 'results' in query_result_example:
            assert_that(query_results.table,
                        has_length(len(
                            query_result_example['results']['bindings'])))
        else:
            assert_that(query_results.table[0],
                        has_key('boolean'))
            assert_that(query_results.table, has_length(1))

    @pytest.mark.parametrize('query_result_example', [
        'sql_select.json',
        'sql_select_missing_value.json'
    ], indirect=True, ids=lambda x: x.split('.')[0])
    def test_dataframe(self, query_result_example, query_results):
        metadata_names = [c['name'] for c in query_result_example['metadata']]
        df = query_results.dataframe
        assert_that(df['st.station_id'].dtype, equal_to('int64'))
        assert_that(df['st.name'].dtype, equal_to('object'))
        assert_that(df['st.lat'].dtype, equal_to('float64'))
        assert_that(df['st.datetime'].dtype, equal_to('datetime64[ns]'))
        assert_that(df.shape,
                    equal_to((len(query_result_example['results']['bindings']),
                              len(metadata_names))))

    def test_str_column(self, query_results):
        '''
        Test added for https://github.com/datadotworld/data.world-py/issues/68
        added a value in the `st.name` column in sql_select.json of "NONE",
        which was previously mapped to Python `None` - this verifies that we
        have fixed that issue.
        '''
        for value in query_results.dataframe['st.name']:
            assert_that(value)

    def test_str(self, query_results, query_result_example):
        assert_that(str(query_results), equal_to(str(query_result_example)))
