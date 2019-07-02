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

try:
    from collections.abc import OrderedDict
except ImportError:
    from collections import OrderedDict

from tableschema import Schema

from datadotworld.models import table_schema


class QueryResults(object):
    """Query results

    Class for accessing and working with the results of a query.

    Attributes
    ----------
    raw_data : str
        Query results as raw SPARQL JSON data
    table : list of rows
        Query results as a `list` of rows.
        Each row is a mapping of field names to their respective values.
    dataframe : `pandas.DataFrame`
        Query results as a `DataFrame`.
    """

    def __init__(self, raw):
        self.raw_data = raw

        self._schema = table_schema.infer_table_schema(raw)

        self._table = None
        self._dataframe = None

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.raw_data))

    def __str__(self):
        return str(self.raw_data)

    def describe(self):
        return self._schema

    @property
    def table(self):
        """Build and cache a table from query results"""
        if self._table is None:
            self._table = list(self._iter_rows())

        return self._table

    @property
    def dataframe(self):
        """Build and cache a dataframe from query results"""

        if self._dataframe is None:
            try:
                import pandas as pd
            except ImportError:
                raise RuntimeError('To enable dataframe support, '
                                   'run \'pip install datadotworld[pandas]\'')

            self._dataframe = pd.DataFrame.from_records(self._iter_rows(),
                                                        coerce_float=True)

        return self._dataframe

    def _iter_rows(self):
        if self._schema is not None:  # Not empty results
            schema_obj = Schema(self._schema)
            if 'results' in self.raw_data:
                field_names = [field.name for field in schema_obj.fields]
                result_vars = self.raw_data['head']['vars']

                for binding in self.raw_data['results']['bindings']:
                    rdf_terms = table_schema.order_terms_in_binding(
                        result_vars, binding)

                    values = []
                    for rdf_term in rdf_terms:
                        if rdf_term is not None:
                            values.append(rdf_term['value'])
                        else:
                            values.append(None)

                    table_row = schema_obj.cast_row(values)

                    # when the column is a string value, the jsontableschema
                    # library is incorrectly mapping the several literal
                    # string values ('null', 'none', '-', etc.) to the python
                    # `None` value - a deeper fix might be to reconsider using
                    # that library, or maybe fixing this issue in that
                    # library (since it's probably not a good idea to render
                    # a number of strings un-representable) - this fixes the
                    # problem for our result sets.  Essentially, this zips
                    # over each result set and checks whether we mapped a
                    # non-null value to `None` in a string field, and if
                    # so it restores the non-null value before continuing
                    table_row = map(lambda field, original, mapped:
                                    original if (not mapped) and original and
                                    field.type == 'string'
                                    else mapped,
                                    schema_obj.fields, values, table_row)

                    yield OrderedDict(zip(field_names, table_row))
            elif 'boolean' in self.raw_data:
                # Results of an ASK query
                yield {'boolean': self.raw_data['boolean']}
