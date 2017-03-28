"""
data.world-py
Copyright 2017 data.world, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the
License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.

This product includes software developed at
data.world, Inc.(http://data.world/).
"""
from __future__ import absolute_import

import pytest
from doublex import assert_that
from hamcrest import equal_to, has_length, contains

from datadotworld.models.query import QueryResults


class TestQueryResults:
    @pytest.fixture()
    def query_results(self, query_result_json):
        return QueryResults(query_result_json)

    @pytest.fixture()
    def query_result_unique_names(self, query_result_json):
        unique_names = []
        for index, name in enumerate(column['name'] for column in
                                     query_result_json['metadata']):
            unique_name = (name + str(index)
                           if name in unique_names else name)
            unique_names.append(unique_name)
        return unique_names

    def test_describe(self, query_result_unique_names, query_results):
        field_names = [f['name'] for f in query_results.describe()['fields']]
        assert_that(field_names, contains(*query_result_unique_names))

    def test_raw_data(self, query_results, query_result_json):
        assert_that(query_results.raw_data, equal_to(query_result_json))

    def test_table(self, query_result_json, query_result_unique_names,
                   query_results):
        for row in query_results.table:
            assert_that(row.keys(), contains(*query_result_unique_names))
            assert_that(row.values(),
                        contains(*(row[f] for f in query_result_unique_names)))
        assert_that(query_results.table,
                    has_length(len(query_result_json['results']['bindings'])))

    def test_dataframe(self, query_result_json, query_result_unique_names,
                       query_results):
        df = query_results.dataframe
        assert_that(df['station_id'].dtype, equal_to('int64'))
        assert_that(df['st.name'].dtype, equal_to('object'))
        assert_that(df['st.lat'].dtype, equal_to('float64'))
        assert_that(df['st.datetime'].dtype, equal_to('datetime64[ns]'))
        assert_that(df.shape,
                    equal_to((len(query_result_json['results']['bindings']),
                              len(query_result_unique_names))))

    def test_str(self, query_results, query_result_json):
        assert_that(str(query_results), equal_to(str(query_result_json)))
