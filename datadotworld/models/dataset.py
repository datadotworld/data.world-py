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

import copy
import os
import warnings
from collections import OrderedDict

import datapackage
import six
from datapackage.resource import TabularResource
from jsontableschema.exceptions import SchemaValidationError
from os import path
from tabulator import Stream

from datadotworld.models.table_schema import (sanitize_resource_schema,
                                              order_columns_in_row,
                                              fields_to_dtypes)
from datadotworld.util import LazyLoadedDict, memoized


class LocalDataset(object):
    """Dataset saved in the local file system

    .. note:: Datasets are packaged for local access in the form of
              Datapackage.
              See specs at http://specs.frictionlessdata.io/data-package/

    Parameters
    ----------
    descriptor_file : str or file-like object
        Path or handle for the descriptor of the dataset (datapackage.json)

    Attributes
    ----------
    raw_data : dict of bytes
        Mapping of resource names to their content (raw bytes) for all types
        of data contained in the dataset.
    tables : dict of tables
        Mapping of resource names to their data table for all *tabular* data
        contained in the dataset.
        A table is a `list` of rows, where each row is a mapping of field
        names to their respective values.
    dataframes : dict of `pandas.DataFrame`
        Mapping of resource names to their `DataFrame` representation for all
        *tabular* data contained  in the dataset.

    """

    def __init__(self, descriptor_file):

        self._datapackage = datapackage.DataPackage(descriptor_file)

        self.__descriptor_file = descriptor_file
        self.__base_path = os.path.dirname(
            os.path.abspath(self.__descriptor_file))

        # Index resources by name
        self.__resources = {r.descriptor['name']: r
                            for r in self._datapackage.resources}
        self.__tabular_resources = {k: sanitize_resource_schema(r)
                                    for (k, r) in self.__resources.items()
                                    if type(r) is TabularResource and
                                    r.descriptor['path'].startswith('data')}
        self.__invalid_schemas = []  # Resource names with invalid schemas

        # All formats
        self.raw_data = LazyLoadedDict.from_keys(
            self.__resources.keys(),
            self._load_raw_data,
            'bytes')

        # Tabular formats
        self.tables = LazyLoadedDict.from_keys(
            self.__tabular_resources.keys(),
            self._load_table,
            type_hint='list of rows')
        self.dataframes = LazyLoadedDict.from_keys(
            self.__tabular_resources.keys(),
            self._load_dataframe,
            type_hint='pandas.DataFrame')

    def describe(self, resource=None):
        """Describe dataset or resource within dataset

        Parameters
        ----------
        resource : str, optional
            The name of a specific resource (i.e. file or table) contained in
            the dataset. If ``resource`` is None, this method will describe
            the dataset itself.

        Returns
        -------
        dict
            The descriptor of the dataset or of a specific resource, if
            ``resource`` is specified in the call.
        """
        if resource is None:
            # Show simpler descriptor, omitting schema definitions
            simple_descriptor = copy.deepcopy(self._datapackage.descriptor)
            for resource in simple_descriptor['resources']:
                resource.pop('schema', None)
            return simple_descriptor
        else:
            return self.__resources[resource].descriptor

    @memoized(key_mapper=lambda self, resource_name: resource_name)
    def _load_raw_data(self, resource_name):
        """Extract raw data from resource"""
        # Instantiating the resource again as a simple `Resource` ensures that
        # ``data`` will be returned as bytes.
        upcast_resource = datapackage.Resource(
            self.__resources[resource_name].descriptor,
            default_base_path=self.__base_path)
        return upcast_resource.data

    @memoized(key_mapper=lambda self, resource_name: resource_name)
    def _load_table(self, resource_name):
        """Build table structure from resource data"""
        tabular_resource = self.__tabular_resources[resource_name]

        try:
            # Sorting fields in the same order as they appear in the schema
            # is necessary for tables to be converted into pandas.DataFrame
            fields = []
            if 'schema' in tabular_resource.descriptor:
                fields = [f['name'] for f in
                          tabular_resource.descriptor['schema']['fields']]
            elif len(tabular_resource.data) > 0:
                fields = tabular_resource.data[0].keys()

            return [order_columns_in_row(fields, row) for row in
                    tabular_resource.data]
        except (SchemaValidationError, ValueError, TypeError) as e:
            warnings.warn(
                'Unable to set column types automatically using {} schema. '
                'Data types may need to be adjusted manually. '
                'Error: {}'.format(resource_name, e))
            self.__invalid_schemas.append(resource_name)
            file_format = tabular_resource.descriptor['format']
            with Stream(six.BytesIO(self.raw_data[resource_name]),
                        format=file_format, headers=1,
                        scheme='stream', encoding='utf-8') as stream:
                return [OrderedDict(zip(stream.headers, row))
                        for row in stream.iter()]

    @memoized(key_mapper=lambda self, resource_name: resource_name)
    def _load_dataframe(self, resource_name):
        """Build pandas.DataFrame from resource data

        Lazy load any optional dependencies in order to allow users to
        use package without installing pandas if so they wish.
        """
        try:
            import pandas
        except ImportError:
            raise RuntimeError('To enable dataframe support, '
                               'run \'pip install datadotworld[pandas]\'')

        tabular_resource = self.__tabular_resources[resource_name]
        field_dtypes = fields_to_dtypes(tabular_resource.descriptor['schema'])

        try:
            return pandas.read_csv(
                path.join(
                    self.__base_path,
                    tabular_resource.descriptor['path']),
                dtype=field_dtypes['other'],
                parse_dates=list(field_dtypes['dates'].keys()),
                infer_datetime_format=True)
        except ValueError as e:
            warnings.warn(
                'Unable to set data frame dtypes automatically using {} '
                'schema. Data types may need to be adjusted manually. '
                'Error: {}'.format(resource_name, e))
            return pandas.read_csv(
                path.join(
                    self.__base_path,
                    tabular_resource.descriptor['path']))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__,
                               repr(self.__descriptor_file))

    def __eq__(self, other):
        return self._datapackage.descriptor == other._datapackage.descriptor
