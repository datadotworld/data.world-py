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

try:
    from collections.abc import OrderedDict, Counter
except ImportError:
    from collections import OrderedDict, Counter

#: Mapping of Table Schema field types to all suitable dtypes (pandas)
from warnings import warn

_TABLE_SCHEMA_DTYPE_MAPPING = {
    'string': 'object',
    'number': 'float64',
    'integer': 'int64',
    'boolean': 'bool',
    'array': 'object',
    'object': 'object',
    'date': 'datetime64[ns]',
    'time': 'object',
    'datetime': 'datetime64[ns]',
    'year': 'int64',
    'yearmonth': 'object',
    'geopoint': 'object',
    'geojson': 'object',
    'duration': 'object',
    'any': 'object'
}

#: Mapping of Table Schema field types to all suitable RDF literal types
_TABLE_SCHEMA_TYPE_MAPPINGS = {
    'boolean': [
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


def fields_to_dtypes(schema):
    """Maps table schema fields types to dtypes separating date fields

    :param schema:
    """
    datetime_types = ['date', 'datetime']
    datetime_fields = {
        f['name']: _TABLE_SCHEMA_DTYPE_MAPPING.get(f['type'], 'object')
        for f in schema['fields']
        if f['type'] in datetime_types}

    other_fields = {
        f['name']: _TABLE_SCHEMA_DTYPE_MAPPING.get(f['type'], 'object')
        for f in schema['fields']
        if f['type'] not in datetime_types}

    return {'dates': datetime_fields, 'other': other_fields}


def sanitize_resource_schema(r):
    """Sanitize table schema for increased compatibility

    Up to version 0.9.0 jsontableschema did not support
    year, yearmonth and duration field types
    https://github.com/frictionlessdata/jsontableschema-py/pull/152

    :param r:
    """
    if 'schema' in r.descriptor:
        r.descriptor['schema'] = _sanitize_schema(r.descriptor['schema'])

    return r


def infer_table_schema(sparql_results_json):
    """Infer Table Schema from SPARQL results JSON

    SPARQL JSON Results Spec:
    https://www.w3.org/TR/2013/REC-sparql11-results-json-20130321

    :param sparql_results_json: SPARQL JSON results of a query
    :returns: A schema descriptor for the inferred schema
    :rtype: dict (json)
    """
    if ('results' in sparql_results_json and
            'bindings' in sparql_results_json['results'] and
            len(sparql_results_json['results']['bindings']) > 0):

        # SQL results include metadata, SPARQL results don't
        result_metadata = sparql_results_json.get('metadata', [])
        metadata_names = [item['name'] for item in result_metadata]
        result_vars = sparql_results_json['head']['vars']

        _verify_unique_names(result_vars, metadata_names)

        # SQL results require var name mapping, SPARQL results vars don't
        result_vars_mapping = dict(zip(
            result_vars, (metadata_names
                          if metadata_names != []
                          else result_vars)))

        homogeneous_types = _get_types_from_sample(
            result_vars, sparql_results_json)

        fields = []
        if homogeneous_types is None:
            for result_var in result_vars:
                fields.append({
                    'name': result_vars_mapping.get(result_var),
                    'type': 'string'
                })
        else:
            for index, var in enumerate(result_vars):
                field = {
                    'name': result_vars_mapping.get(var),
                    'type': infer_table_schema_type_from_rdf_term(
                        homogeneous_types[var].get('type'),
                        homogeneous_types[var].get('datatype')
                    )}

                if 'datatype' in homogeneous_types.get(var):
                    field['rdfType'] = homogeneous_types[var].get('datatype')

                term_metadata = (result_metadata[index]
                                 if result_metadata != [] else {})
                if 'description' in term_metadata:
                    field['description'] = term_metadata['description']

                fields.append(field)

        return _sanitize_schema({'fields': fields})
    elif 'boolean' in sparql_results_json:
        # ASK query results
        return {'fields': [{'name': 'boolean', 'type': 'boolean'}]}
    else:
        warn('Unable to infer table schema from empty query results')
        return None


def infer_table_schema_type_from_rdf_term(term_type, term_datatype):
    """Map an RDF literal type to Table Schema field type

    :param term_type: type from RDF term
    :param term_datatype: datatype from RDF term
    """
    if (term_type == 'literal' and
            term_datatype is not None):
        return _RDF_LITERAL_TYPE_MAPPING.get(term_datatype,
                                             'string')
    else:
        return 'string'


def order_columns_in_row(fields, unordered_row):
    """Ensure columns appear in the same order for every row in table

    :param fields:
    :param unordered_row:
    """
    fields_idx = {f: pos for pos, f in enumerate(fields)}
    return OrderedDict(sorted(unordered_row.items(),
                              key=lambda i: fields_idx[i[0]]))


def order_terms_in_binding(result_vars, binding):
    """Convert a binding into a complete ordered list of terms ordered
    in accordance with result_vars

    :param result_vars: Vars list from SPARQL JSON results
    :param binding: Item in bindings section of SPARQL results JSON
    :returns: A list of RDF terms
    :rtype: list
    """
    return [binding.get(result_var) for result_var in result_vars]


def _sanitize_schema(schema_descriptor):
    """

    :param schema_descriptor:
    """
    missing_type_support = False
    try:
        from tableschema import YearType, YearMonthType, DurationType  # noqa
    except ImportError:
        missing_type_support = True

    for field in schema_descriptor.get('fields', []):
        # Datapackage specs were changed along the way
        # Convert gyear and gyearmonth to year and yearmonth
        # https://github.com/frictionlessdata/specs/pull/370
        if field.get('type') in ['gyear', 'gyearmonth']:
            field['type'] = field['type'][1:]

        # Default datetime field format must fit pattern: '%Y-%m-%dT%H:%M:%SZ'
        # However, data.world may fail to include 'Z' at the end
        if field['type'] == 'datetime' and 'format' not in field:
            field['format'] = 'any'

        if missing_type_support:
            # Convert unsupported types to integer and string
            # as appropriate
            type_mapping = {
                'integer': ['year', 'yearmonth'],
                'string': ['duration']}

            for old_type, new_types in type_mapping.items():
                if field.get('type') in new_types:
                    field['type'] = old_type

    return schema_descriptor


def _verify_unique_names(result_vars, metadata_names):
    """

    :param result_vars:
    :param metadata_names:
    """
    metadata_name_duplicates = [name_duplicate
                                for name_duplicate, count
                                in Counter(metadata_names).items()
                                if count > 1]
    var_duplicates = [var_duplicate
                      for var_duplicate, count
                      in Counter(result_vars).items()
                      if count > 1]
    if (metadata_name_duplicates != [] or
            var_duplicates != []):
        raise ValueError('Ambiguous query results. '
                         'One or more columns appear multiple times: '
                         '{}'.format(metadata_name_duplicates or
                                     var_duplicates))


def _get_types_from_sample(result_vars, sparql_results_json):
    """Return types if homogenous within sample

    Compare up to 10 rows of results to determine homogeneity.

    DESCRIBE and CONSTRUCT queries, for example,

    :param result_vars:
    :param sparql_results_json:
    """
    total_bindings = len(sparql_results_json['results']['bindings'])
    homogeneous_types = {}
    for result_var in result_vars:
        var_types = set()
        var_datatypes = set()
        for i in range(0, min(total_bindings, 10)):
            binding = sparql_results_json['results']['bindings'][i]
            rdf_term = binding.get(result_var)
            if rdf_term is not None:  # skip missing values
                var_types.add(rdf_term.get('type'))
                var_datatypes.add(rdf_term.get('datatype'))
        if len(var_types) > 1 or len(var_datatypes) > 1:
            return None  # Heterogeneous types
        else:
            homogeneous_types[result_var] = {
                'type': var_types.pop() if var_types else None,
                'datatype': var_datatypes.pop() if var_datatypes else None
            }

    return homogeneous_types
