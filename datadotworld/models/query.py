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

import six
from tabulator import Stream


class QueryResults(object):
    """Query results

    Class for accessing and working with the results of a query.

    Attributes
    ----------
    raw_data : str
        Query results as raw CSV data.
    table : iterable
        Query results as a series of rows.
        Each row is a `dict` where keys are column names and values their respective value.
    dataframe : `pandas.DataFrame`
        Query results as a `DataFrame`.
    """

    def __init__(self, raw):
        self.raw_data = raw

    def __str__(self):
        return self.raw_data

    @property
    def dataframe(self):
        import pandas as pd
        return pd.DataFrame.from_csv(six.StringIO(self.raw_data), index_col=False)

    @property
    def table(self):
        # TODO Return typed values based on data.world type inference
        stream = Stream(self.raw_data, headers=1, format='csv', scheme='text')
        stream.open()

        return stream.iter(keyed=True)
