import csv
from collections.abc import Mapping

import datapackage
import requests
from datapackage.resource import TabularResource


class LocalDataset():
    def __init__(self, descriptor_file):
        self._descriptor_file = descriptor_file
        self._datapackage = datapackage.DataPackage(descriptor_file)

        self._resources = {r.descriptor['name']: r for r in self._datapackage.resources}

        table_resources = {k: r for (k, r) in self._resources.items() if type(r) is TabularResource}
        other_resources = {k: r for (k, r) in self._resources.items() if type(r) is not TabularResource}

        self.tables = LazyReadOnlyDict(table_resources, to_data)
        self.dataframes = LazyReadOnlyDict(table_resources, to_dataframe)
        self.raw = LazyReadOnlyDict(other_resources, to_data)

    def describe(self, resource=None):
        if resource is None:
            return self._datapackage.descriptor
        else:
            return self._resources[resource].descriptor


class LazyReadOnlyDict(Mapping):
    def __init__(self, resources, lazy_reader):
        self._resources = resources
        self._data_extractor = lazy_reader
        self._cache = {}

    def __getitem__(self, item):
        if item not in self._cache:
            self._cache[item] = self._data_extractor(self._resources[item])
        return self._cache[item]

    def __iter__(self):
        for k in self._resources.keys():
            yield k

    def __len__(self):
        return len(self._resources)

    def __str__(self):
        return str({k: self._cache.get(k) or LazyLoadedValuePlaceholder() for k in self._resources.keys()})


class LazyLoadedValuePlaceholder:
    """Just a place holder for LazyLoadedReadOnlyDict values"""


def to_data(resource):
    return resource.data


def to_dataframe(resource):
    import pandas
    data = resource.local_data_path or requests.get(resource.remote_data_path, stream=True).raw
    dtypes = to_dataframe_types(resource.descriptor['schema']['fields'])
    dialect = to_csv_dialect(resource.descriptor.get('dialect'))
    return pandas.read_csv(data, dtype=dtypes, dialect=dialect)


def to_dataframe_types(table_schema_fields):
    datapackage_to_dataframe_map = {
        'string': 'object',
        'number': 'float',
        'integer': 'int',
        'date': 'object',
        'time': 'object',
        'datetime': 'datetime64[ns, tz]',
        'year': 'category',
        'yearmonth': 'category',
        'boolean': 'bool',
        'object': 'object',
        'geopoint': 'object',
        'geojson': 'object',
        'array': 'object',
        'duration': 'timedelta[ns]',
        'any': 'object'
    }
    return {f['name']: datapackage_to_dataframe_map.get(f['type'], 'object') for f in table_schema_fields}


def to_csv_dialect(table_resource_dialect):
    if table_resource_dialect is None:
        return csv.excel()

    dialect = csv.excel()
    dialect.delimiter = table_resource_dialect.get('delimiter', dialect.delimiter)
    dialect.doublequote = table_resource_dialect.get('doubleQuote', dialect.doublequote)
    dialect.lineterminator = table_resource_dialect.get('lineTerminator', dialect.lineterminator)
    dialect.quotechar = table_resource_dialect.get('quoteChar', dialect.quotechar)
    dialect.escapechar = table_resource_dialect.get('escapeChar', dialect.escapechar)
    dialect.skipinitialspace = table_resource_dialect.get('skipInitialSpace', dialect.skipinitialspace)

    return dialect
