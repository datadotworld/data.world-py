import os

import datapackage
import six
from datapackage.resource import TabularResource
from jsontableschema_pandas import Storage

from datadotworld.util import LazyLoadedDict

if six.PY2:
    pass
else:
    pass


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
        self.__base_path = os.path.dirname(os.path.abspath(self.__descriptor_file))

        # Index resources by name
        self.__resources = {r.descriptor['name']: r for r in self._datapackage.resources}

        # Initialize jsontableschema_pandas storage to convert data into dataframes on demand
        tabular_resources = {k: r for (k, r) in self.__resources.items() if type(r) is TabularResource}
        self.__storage = Storage()
        self.__storage.create(tabular_resources.keys(),
                              [r.descriptor['schema'] for r in tabular_resources.values() if 'schema' in r.descriptor])

        # All resources
        self.raw_data = LazyLoadedDict(self.__resources.keys(), self._to_data, 'bytes')

        # Tabular resources
        self.tables = LazyLoadedDict(tabular_resources.keys(), lambda key: tabular_resources[key].data,
                                     type_hint='iterable')
        self.dataframes = LazyLoadedDict(tabular_resources.keys(), self._to_dataframe, type_hint='pandas.DataFrame')

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

    def _to_data(self, resource_name):
        """Extract raw data from resource"""
        # Instantiating the resource again as a simple `Resource` ensures that ``data`` will be returned as bytes.
        upcast_resource = datapackage.Resource(self.__resources[resource_name].descriptor,
                                               default_base_path=self.__base_path)
        return upcast_resource.data

    def _to_dataframe(self, resource_name):
        """Extract dataframe from tabular resource"""
        if self.__storage[resource_name].size == 0:
            self.__storage.write(resource_name, [row.values() for row in self.tables[resource_name]])
        return self.__storage[resource_name]

    def __repr__(self):
        fully_qualified_type = '{}.{}'.format(self.__module__, self.__class__.__name__)
        return '{}({})'.format(fully_qualified_type, repr(self.__descriptor_file))
