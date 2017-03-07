import csv
from io import StringIO

import datapackage


class LocalDataset():
    def __init__(self, descriptor_file):
        self._descriptor_file = descriptor_file
        self._datapackage = datapackage.DataPackage(descriptor_file)

    @property
    def descriptor(self):
        return self._datapackage.descriptor

    @property
    def files(self):
        return {r.descriptor['name']: r.local_data_path
                for r in self._datapackage.resources if r.local_data_path is not None}

    @property
    def file_links(self):
        return {r.descriptor['name']: r.remote_data_path
                for r in self._datapackage.resources if r.local_data_path is None and r.remote_data_path is not None}

    @property
    def tables(self):
        if not hasattr(self, '_tables'):
            store = datapackage.push_datapackage(self._descriptor_file, 'pandas')
            self._tables = {b: LocalTable(store.describe(b), store[b]) for b in store.buckets}
        return self._tables


class LocalTable():
    def __init__(self, descriptor, dataframe):
        self.descriptor = descriptor
        self._dataframe = dataframe

    def as_dataframe(self):
        return self._dataframe

    def as_string(self):
        buffer = StringIO()
        self._dataframe.to_csv(buffer)
        return buffer.getvalue()

    def as_csv(self):
        return csv.reader(self.as_stream())

    def as_stream(self):
        buffer = StringIO()
        self._dataframe.to_csv(buffer)
        return buffer
