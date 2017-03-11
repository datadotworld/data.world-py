import os

import datapackage
import six
from datapackage.resource import TabularResource
from jsontableschema_pandas import Storage

if six.PY2:
    from collections import Mapping
else:
    from collections.abc import Mapping


class LocalDataset():
    """Class for accessing and working with a data.world dataset stored in the local filesystem

    .. note:: Datasets are packaged for local access in the form of Datapackage.
              See specs at http://specs.frictionlessdata.io/data-package/

    Parameters
    ----------
    descriptor_file : str or file-like object
        Path or handle for the descriptor of the dataset (datapackage.json)

    Attributes
    ----------
    raw_data : dict of bytes
        Mapping of resource names to their content (raw bytes) for all types of data contained in the dataset.
    tables : dict of tables
        Mapping of resource names to their rows for all *tabular* data contained in the dataset.
    dataframes : dict of `pandas.DataFrame`
        Mapping of resource names to their `DataFrame` representation for all *tabular* data contained  in the dataset.

    """

    def __init__(self, descriptor_file):

        self._datapackage = datapackage.DataPackage(descriptor_file)
        self.__descriptor_file = descriptor_file

        # Index resources by name
        self.__resources = {r.descriptor['name']: r for r in self._datapackage.resources}

        table_resources = {k: r for (k, r) in self.__resources.items() if type(r) is TabularResource}

        # Initialize jsontableschema_pandas storage to convert data into dataframes on demand
        storage = Storage()
        storage.create(self.__resources.keys(),
                       [r.descriptor['schema'] for r in self.__resources.values() if 'schema' in r.descriptor])

        # All resources
        base_path = os.path.dirname(os.path.abspath(self.__descriptor_file))
        self.raw_data = LazyLoadedResourceDict(self.__resources,
                                               lambda resource: LocalDataset._to_data(resource, base_path),
                                               'bytes')

        # Tabular resources
        self.tables = LazyLoadedResourceDict(table_resources, LocalDataset._to_data, type_hint='iterable')
        self.dataframes = LazyLoadedResourceDict(table_resources,
                                                 lambda resource: LocalDataset._to_dataframe(storage, resource),
                                                 type_hint='pandas.DataFrame')

    def describe(self, resource=None):
        """Describe dataset or resource within dataset

        Parameters
        ----------
        resource : str, optional
            The name of a specific resource (i.e. file or table) contained in the dataset.

        Returns
        -------
        dict
            The descriptor of the dataset or of a specific resource, if ``resource`` is specified in the call.
        """
        if resource is None:
            return self._datapackage.descriptor
        else:
            return self.__resources[resource].descriptor

    @staticmethod
    def _to_data(resource, base_path):
        """Extract raw data from resource"""
        # Instantiating the resource again as a simple `Resource` ensures that ``data`` will be returned as bytes.
        return datapackage.Resource(resource.descriptor, default_base_path=base_path).data

    @staticmethod
    def _to_dataframe(storage, resource):
        """Extract dataframe from tabular resource"""
        name = resource.descriptor['name']
        if storage[name].size == 0:
            storage.write(name, LocalDataset._to_rows_iter(resource.data))
        return storage[name]

    @staticmethod
    def _to_rows_iter(table):
        """Extract table rows as lists"""
        for row in table:
            yield row.values()

    def __repr__(self):
        fully_qualified_type = '{}.{}'.format(self.__module__, self.__class__.__name__)
        return '{}({})'.format(fully_qualified_type, repr(self.__descriptor_file))


class LazyLoadedResourceDict(Mapping):
    """Custom immutable dict implementation with lazy loaded values

    Parameters
    ----------
    resources : list of `datapackage.Resource`
        Datapackage resources
    lazy_loader : function
        Function used to instantiate/load the value for a given key, on demand
    type_hint : str
        String describing the type of the lazy loaded value. Used in place of the value before value is loaded.
    """

    def __init__(self, resources, lazy_loader, type_hint='unknown'):
        self._resources = resources
        self._data_extractor = lazy_loader
        self._type_hint = type_hint
        self.__cache = {}

    def __getitem__(self, item):
        if item not in self.__cache:
            self.__cache[item] = self._data_extractor(self._resources[item])
        return self.__cache[item]

    def __iter__(self):
        for k in self._resources.keys():
            yield k

    def __len__(self):
        return len(self._resources)

    def __repr__(self):
        fully_qualified_type = '{}.{}'.format(self.__module__, self.__class__.__name__)
        return '<{} with values of type: {}>'.format(fully_qualified_type, self._type_hint)

    def __str__(self):
        def format_value_str(resource_key):
            if resource_key in self.__cache.keys():
                return str(self.__cache.get(resource_key))
            else:
                '<{}>'.format(self._type_hint)

        key_value_strings = ["{}: {}".format(k, format_value_str(k)) for k in self._resources.keys()]
        return '{{{}}}'.format(', '.join(key_value_strings))
