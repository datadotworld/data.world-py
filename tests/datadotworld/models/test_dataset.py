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

import copy
from os import path

import pytest
from datadotworld.models.dataset import LocalDataset
from datadotworld.models.table_schema import sanitize_resource_schema
from datapackage import DataPackage, Resource
from doublex import assert_that, is_
from hamcrest import equal_to, contains, calling, not_, raises, not_none


class TestLocalDataset:
    @pytest.fixture()
    def simpsons_descriptor_path(self, test_datapackages_path):
        return path.join(test_datapackages_path, 'the-simpsons-by-the-data',
                         'datapackage.json')

    @pytest.fixture()
    def simpsons_datapackage(self, simpsons_descriptor_path):
        datapackage = DataPackage(descriptor=simpsons_descriptor_path)
        for r in datapackage.resources:
            sanitize_resource_schema(r)
        return datapackage

    @pytest.fixture()
    def simpsons_dataset(self, simpsons_descriptor_path):
        return LocalDataset(simpsons_descriptor_path)

    @pytest.fixture()
    def simpsons_broken_descriptor_path(self, test_datapackages_path):
        return path.join(test_datapackages_path,
                         'the-simpsons-by-the-data-bad-schema',
                         'datapackage.json')

    @pytest.fixture()
    def simpsons_broken_datapackage(self, simpsons_broken_descriptor_path):
        return DataPackage(descriptor=simpsons_broken_descriptor_path)

    @pytest.fixture()
    def simpsons_broken_dataset(self, simpsons_broken_descriptor_path):
        return LocalDataset(simpsons_broken_descriptor_path)

    def test_describe(self, simpsons_dataset, simpsons_datapackage):
        simple_descriptor = copy.deepcopy(simpsons_datapackage.descriptor)
        for resource in simple_descriptor['resources']:
            resource.pop('schema', None)
        assert_that(simpsons_dataset.describe(),
                    equal_to(simple_descriptor))

    def test_describe_resource(self, simpsons_dataset, simpsons_datapackage):
        for r in simpsons_datapackage.resources:
            assert_that(simpsons_dataset.describe(r.descriptor['name']),
                        equal_to(r.descriptor))

    def test_raw_data(self, simpsons_dataset, simpsons_datapackage,
                      simpsons_descriptor_path):
        for r in simpsons_datapackage.resources:
            resource = Resource(r.descriptor, default_base_path=path.dirname(
                simpsons_descriptor_path))
            once = simpsons_dataset.raw_data[r.descriptor['name']]
            twice = simpsons_dataset.raw_data[r.descriptor['name']]
            assert_that(once, equal_to(resource.data))
            # Not a generator
            for _ in once:
                pass  # Consume iterable
            assert_that(once, equal_to(twice))

    def test_tables(self, simpsons_dataset, simpsons_datapackage):
        for r in simpsons_datapackage.resources:
            if r.descriptor['name'] in simpsons_dataset.tables:
                once = simpsons_dataset.tables[r.descriptor['name']]
                twice = simpsons_dataset.tables[r.descriptor['name']]
                assert_that(once, equal_to(r.data))
                # Same keys and values in consistent order
                first_row_fields = once[0].keys()
                for row in once:
                    assert_that(row.keys(), contains(*first_row_fields))
                    ordered_values = [row[f] for f in first_row_fields]
                    assert_that(row.values(), contains(*ordered_values))
                assert_that(once, equal_to(twice))

    def test_tables_broken_schema(self, simpsons_broken_dataset):
        assert_that(calling(simpsons_broken_dataset.tables.get).with_args(
            'simpsons_episodes'), not_(raises(Exception)))
        assert_that(simpsons_broken_dataset.tables.get('simpsons_episodes'),
                    not_none())

    def test_dataframes(self, simpsons_dataset):
        for k, t in simpsons_dataset.tables.items():
            once = simpsons_dataset.dataframes[k]
            twice = simpsons_dataset.dataframes[k]
            assert_that(once.shape, equal_to((len(t), len(t[0]))))
            assert_that(once.equals(twice), is_(True))

    def test_dataframe_types(self, simpsons_dataset):
        df = simpsons_dataset.dataframes['simpsons_episodes']
        assert_that(df['id'].dtype, equal_to('int64'))
        assert_that(df['title'].dtype, equal_to('object'))
        assert_that(df['original_air_date'].dtype, equal_to('datetime64[ns]'))
        assert_that(df['original_air_year'].dtype, equal_to('int64'))
        assert_that(df['imdb_rating'].dtype, equal_to('float64'))

    def test_dataframe_broken_schema(self, simpsons_broken_dataset):
        assert_that(calling(simpsons_broken_dataset.dataframes.get).with_args(
            'simpsons_episodes'), not_(raises(Exception)))
        assert_that(simpsons_broken_dataset.dataframes.get(
            'simpsons_episodes'), not_none())

    def test_repr(self, simpsons_dataset):
        # noinspection PyUnresolvedReferences
        import datadotworld
        assert_that(simpsons_dataset, equal_to(eval(repr(simpsons_dataset))))
