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

import pytest

from datadotworld.models.query import QueryResults
from doublex import assert_that
from hamcrest import equal_to, only_contains


class TestQueryResults:
    @pytest.fixture()
    def query_results(self, query_result_csv):
        return QueryResults(query_result_csv)

    def test_raw_data(self, query_results, query_result_csv):
        assert_that(query_results.raw_data, equal_to(query_result_csv))

    def test_table(self, query_results):
        expected = ({'cool': '1', 'beans': '2'}, {'cool': '3', 'beans': '4'})
        assert_that(list(query_results.table), only_contains(*expected))

    def test_dataframe(self, query_results):
        df = query_results.dataframe
        assert_that(df.shape, equal_to((2, 2)))
        # TODO More comprehensive assertions

    def test_str(self, query_results, query_result_csv):
        assert_that(str(query_results), equal_to(query_result_csv))