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
from __future__ import absolute_import

from collections import OrderedDict

from jsontableschema import Schema

from datadotworld.models.util import sanitize_schema

#: Mapping of Table Schema field types to all suitable RDF literal types
_TABLE_SCHEMA_TYPE_MAPPINGS = {
    'bool': [
        'http://www.w3.org/2001/XMLSchema#boolean'
    ],
    'integer': [
        'http://www.w3.org/2001/XMLSchema#integer',
        'http://www.w3.org/2001/XMLSchema#nonPositiveInteger',
        'http://www.w3.org/2001/XMLSchema#nonNegativeInteger',
        'http://www.w3.org/2001/XMLSchema#negativeInteger',
        'http://www.w3.org/2001/XMLSchema#long',
        'http://www.w3.org/2001/XMLSchema#int',
        'http://www.w3.org/2001/XMLSchema#short',
        'http://www.w3.org/2001/XMLSchema#byte',
        'http://www.w3.org/2001/XMLSchema#unsignedLong',
        'http://www.w3.org/2001/XMLSchema#unsignedInt',
        'http://www.w3.org/2001/XMLSchema#unsignedShort',
        'http://www.w3.org/2001/XMLSchema#unsignedByte',
        'http://www.w3.org/2001/XMLSchema#positiveInteger'
    ],
    'number': [
        'http://www.w3.org/2001/XMLSchema#decimal',
        'http://www.w3.org/2001/XMLSchema#float',
        'http://www.w3.org/2001/XMLSchema#double'
    ],
    'date': ['http://www.w3.org/2001/XMLSchema#date'],
    'datetime': [
        'http://www.w3.org/2001/XMLSchema#dateTime',
        'http://www.w3.org/2001/XMLSchema#dateTimeStamp'
    ],
    'time': ['http://www.w3.org/2001/XMLSchema#time'],
    'duration': [
        'http://www.w3.org/2001/XMLSchema#duration',
        'http://www.w3.org/2001/XMLSchema#dayTimeDuration',
        'http://www.w3.org/2001/XMLSchema#yearMonthDuration'
    ],
    'year': ['http://www.w3.org/2001/XMLSchema#gYear'],
    'yearmonth': ['http://www.w3.org/2001/XMLSchema#gYearMonth']
}

#: Mapping of RDF literal types to a single suitable Table Schema field type
_RDF_LITERAL_TYPE_MAPPING = {xsd_type: ts_type
                             for ts_type, xsd_types
                             in _TABLE_SCHEMA_TYPE_MAPPINGS.items()
                             for xsd_type in xsd_types}


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

        inferred_schema = self._infer_schema_from_results(raw)
        sanitize_schema(inferred_schema)
        self._schema = inferred_schema

        self._table = None
        self._storage = None

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.raw_data))

    def __str__(self):
        return str(self.raw_data)

    def describe(self):
        return self._schema

    @property
    def dataframe(self):
        try:
            from jsontableschema_pandas import Storage
        except ImportError:
            raise RuntimeError('To enable dataframe support, '
                               'run \'pip install datadotworld[PANDAS]\'')

        if self._storage is None:
            self._storage = Storage()
            self._storage.create('results', self._schema)

            row_values = [row.values() for row in self.table]
            self._storage.write('results', row_values)

        return self._storage['results']

    @property
    def table(self):
        if self._table is None:
            schema_obj = Schema(self._schema)
            field_names = [field.name for field in schema_obj.fields]
            result_vars = self.raw_data['head']['vars']

            table = []
            for binding in self.raw_data['results']['bindings']:
                values = [rdf_term['value']
                          for rdf_term in
                          self._unwrap_binding(result_vars, binding)]
                table_row = schema_obj.cast_row(values)
                table.append(OrderedDict(zip(field_names, table_row)))

            self._table = table

        return self._table

    def _infer_schema_from_results(self, sparql_results_json):
        """Infer Table Schema from SPARQL results JSON

        SPARQL JSON Results Spec:
        https://www.w3.org/TR/2013/REC-sparql11-results-json-20130321

        Parameters
        ----------
        sparql_results_json
            SPARQL JSON results of a query

        Returns
        -------
        dict (json)
            A schema descriptor for the inferred schema
        """
        if ('results' in sparql_results_json and
                    'bindings' in sparql_results_json['results'] and
                    len(sparql_results_json['results']['bindings']) > 0):

            result_metadata = sparql_results_json['metadata']
            result_vars = sparql_results_json['head']['vars']
            first_binding = sparql_results_json['results']['bindings'][0]

            fields = []
            unique_field_names = set()
            for index, rdf_term in enumerate(
                    self._unwrap_binding(result_vars, first_binding)):

                # Ensures unique field names
                field_name = result_metadata[index]['name']
                if field_name in unique_field_names:
                    field_name += str(index)
                unique_field_names.add(field_name)

                field = {
                    'name': field_name,
                    'type': self._infer_table_schema_type_from_rdf_term(
                        rdf_term)
                }

                if 'description' in result_metadata[index]:
                    field['description'] = result_metadata[index][
                        'description']

                fields.append(field)

            return {'fields': fields}
        else:
            raise ValueError(
                'Unable to infer table schema from empty query results')

    @staticmethod
    def _infer_table_schema_type_from_rdf_term(rdf_term):
        """Map an RDF literal type to Table Schema field type

        Parameters
        ----------
        rdf_term
            A value of an item in a binding. A binding is an item in the
            bindings section of the SPARQL results JSON.

        Returns
        -------
        str
            A Table Schema field type
        """
        if (rdf_term['type'] == 'literal' and
                    rdf_term.get('datatype') is not None):
            return _RDF_LITERAL_TYPE_MAPPING.get(rdf_term['datatype'],
                                                 'string')
        else:
            return 'string'

    @staticmethod
    def _unwrap_binding(result_vars, binding):
        """Convert a binding into a list ordered in accordance with result_vars

        Parameters
        ----------
        result_vars
            Vars list from SPARQL JSON results
        binding
            Item in bindings section of SPARQL results JSON

        Returns
        -------
        list
            A list of RDF terms
        """
        return [binding[result_var] for result_var in result_vars]
