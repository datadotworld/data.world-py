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
import copy
import csv
import os
import warnings

import datapackage
import pandas
import six
from datapackage.resource import TabularResource

from datadotworld.util import LazyLoadedDict


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
        Mapping of resource names to their rows for all *tabular* data
        contained in the dataset.
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
        self.__resources = {r.descriptor['name']: r for r in
                            self._datapackage.resources}
        self.__tabular_resources = {k: r for (k, r) in self.__resources.items()
                                    if type(r) is TabularResource}
        self.__invalid_schemas = []  # Resource names with invalid schemas

        # All formats
        self.raw_data = LazyLoadedDict(self.__resources.keys(),
                                       self._to_raw_data,
                                       'bytes')

        # Tabular formats
        self.tables = LazyLoadedDict(self.__tabular_resources.keys(),
                                     self.__to_table,
                                     type_hint='iterable')
        self.dataframes = LazyLoadedDict(self.__tabular_resources.keys(),
                                         self._to_dataframe,
                                         type_hint='pandas.DataFrame')

    def describe(self, resource=None):
        """Describe dataset or resource within dataset

        Parameters
        ----------
        resource : str, optional
            The name of a specific resource (i.e. file or table) contained in
            the dataset.

        Returns
        -------
        dict
            The descriptor of the dataset or of a specific resource, if
            ``resource`` is specified in the call.
        """
        if resource is None:
            simple_descriptor = copy.deepcopy(self._datapackage.descriptor)
            for resource in simple_descriptor['resources']:
                resource.pop('schema', None)
            return simple_descriptor
        else:
            return self.__resources[resource].descriptor

    def _to_raw_data(self, resource_name):
        """Extract raw data from resource"""
        # Instantiating the resource again as a simple `Resource` ensures that
        # ``data`` will be returned as bytes.
        upcast_resource = datapackage.Resource(
            self.__resources[resource_name].descriptor,
            default_base_path=self.__base_path)
        return upcast_resource.data

    def __to_table(self, resource_name):
        try:
            return self.__tabular_resources[resource_name].data
        except ValueError:
            warnings.warn('Unable to apply datapackage table schema.'
                          'Reverting to strings...')
            self.__invalid_schemas.append(resource_name)
            f = (line.decode('utf-8')
                 for line in six.BytesIO(self.raw_data[resource_name]))
            data = list(csv.DictReader(f))
            return data

    def _to_dataframe(self, resource_name):
        """Extract dataframe from tabular resource"""
        self.__initialize_storage()

        rows = self.tables[resource_name]

        # self.tables will return each row as a dict (no guaranteed order)
        # Below, each row is recreated as a list, using the order of the
        # fields in the schema
        resource_schema = self.describe(resource_name).get('schema')
        ordered_field_names = [field['name'] for field in
                               resource_schema['fields']]
        ordered_rows = [[row[field] for field in ordered_field_names]
                        for row in rows]
        if resource_name not in self.__invalid_schemas:
            if self.__storage[resource_name].size == 0:
                self.__storage.write(resource_name, ordered_rows)
            return self.__storage[resource_name]
        else:
            return pandas.DataFrame(ordered_rows, columns=ordered_field_names)

    def __initialize_storage(self):
        try:
            from jsontableschema_pandas import Storage
        except ImportError:
            raise RuntimeError('To enable dataframe support for datapackages, '
                               'please install the jsontableschema_pandas '
                               'package first.')

        # Initialize storage if needed
        if not hasattr(self, '__storage'):
            self.__storage = Storage()
            for (k, r) in self.__tabular_resources.items():
                if 'schema' in r.descriptor:
                    self.__storage.create(k, r.descriptor['schema'])

    def __repr__(self):
        fully_qualified_type = '{}.{}'.format(self.__module__,
                                              self.__class__.__name__)
        return '{}({})'.format(fully_qualified_type,
                               repr(self.__descriptor_file))

    def __eq__(self, other):
        return self._datapackage.descriptor == other._datapackage.descriptor
