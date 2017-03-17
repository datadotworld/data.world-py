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
import os

import datapackage
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

        # All resources
        self.raw_data = LazyLoadedDict(self.__resources.keys(), self._to_data,
                                       'bytes')

        # Tabular resources
        self.tables = LazyLoadedDict(self.__tabular_resources.keys(),
                                     lambda key: self.__tabular_resources[
                                         key].data,
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
            return self._datapackage.descriptor
        else:
            return self.__resources[resource].descriptor

    def _to_data(self, resource_name):
        """Extract raw data from resource"""
        # Instantiating the resource again as a simple `Resource` ensures that
        # ``data`` will be returned as bytes.
        upcast_resource = datapackage.Resource(
            self.__resources[resource_name].descriptor,
            default_base_path=self.__base_path)
        return upcast_resource.data

    def _to_dataframe(self, resource_name):
        """Extract dataframe from tabular resource"""

        from jsontableschema_pandas import Storage
        # Initialize storage if needed
        if not hasattr(self, '__storage'):
            self.__storage = Storage()
            for (k, r) in self.__tabular_resources.items():
                if 'schema' in r.descriptor:
                    self.__storage.create(k, r.descriptor['schema'])

        if self.__storage[resource_name].size == 0:
            resource_schema = self.describe(resource_name).get('schema')
            ordered_field_names = [field['name'] for field in
                                   resource_schema['fields']]
            # self.tables will return each row as a dict (no guaranteed order)
            # The list comprehension below recreates each row as a list, using
            # the order of the fields in the schema
            self.__storage.write(resource_name,
                                 [[row[field] for field in ordered_field_names]
                                  for row in self.tables[resource_name]])

        return self.__storage[resource_name]

    def __repr__(self):
        fully_qualified_type = '{}.{}'.format(self.__module__,
                                              self.__class__.__name__)
        return '{}({})'.format(fully_qualified_type,
                               repr(self.__descriptor_file))

    def __eq__(self, other):
        return self._datapackage.descriptor == other._datapackage.descriptor
