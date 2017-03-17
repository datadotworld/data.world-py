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
data.world, Inc.(http://www.data.world/).
"""
from __future__ import absolute_import

from os import path

import pytest
from datapackage import DataPackage, Resource
from doublex import assert_that
from hamcrest import equal_to

from datadotworld.models.dataset import LocalDataset


class TestLocalDataset:
    @pytest.fixture()
    def simpsons_descriptor_path(self, test_files_path):
        return path.join(test_files_path, 'the-simpsons-by-the-data',
                         'datapackage.json')

    @pytest.fixture()
    def simpsons_datapackage(self, simpsons_descriptor_path):
        return DataPackage(descriptor=simpsons_descriptor_path)

    @pytest.fixture()
    def simpsons_dataset(self, simpsons_descriptor_path):
        return LocalDataset(simpsons_descriptor_path)

    def test_describe(self, simpsons_dataset, simpsons_datapackage):
        assert_that(simpsons_dataset.describe(),
                    equal_to(simpsons_datapackage.descriptor))

    def test_describe_resource(self, simpsons_dataset, simpsons_datapackage):
        for r in simpsons_datapackage.resources:
            assert_that(simpsons_dataset.describe(r.descriptor['name']),
                        equal_to(r.descriptor))

    def test_raw_data(self, simpsons_dataset, simpsons_datapackage,
                      simpsons_descriptor_path):
        for r in simpsons_datapackage.resources:
            resource = Resource(r.descriptor, default_base_path=path.dirname(
                simpsons_descriptor_path))
            assert_that(simpsons_dataset.raw_data[r.descriptor['name']],
                        equal_to(resource.data))

    def test_tables(self, simpsons_dataset, simpsons_datapackage):
        for r in simpsons_datapackage.resources:
            if r.descriptor['name'] in simpsons_dataset.tables:
                assert_that(simpsons_dataset.tables[r.descriptor['name']],
                            equal_to(r.data))

    def test_dataframes(self, simpsons_dataset):
        for k, t in simpsons_dataset.tables.items():
            df = simpsons_dataset.dataframes[k]
            assert_that(df.shape, equal_to((len(t), len(t[0]))))

    def test_dataframe_types(self, simpsons_dataset):
        df = simpsons_dataset.dataframes['simpsons_episodes']
        assert_that(df['id'].dtype, equal_to('int64'))
        assert_that(df['title'].dtype, equal_to('object'))
        # TODO test different datapackages and more dtypes

    def test_repr(self, simpsons_dataset):
        # noinspection PyUnresolvedReferences
        import datadotworld
        assert_that(simpsons_dataset, equal_to(eval(repr(simpsons_dataset))))
