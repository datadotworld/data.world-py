from collections import OrderedDict


# Datapackage

def patch_jsontableschema_pandas(mappers):
    """Monkey patch jsontableschema_pandas module

    Up to version 0.2.0 jsontableschema_pandas mapped date fields
    to object dtype
    https://github.com/frictionlessdata/
        jsontableschema-pandas-py/pull/23
    """
    if hasattr(mappers, 'jtstype_to_dtype'):
        mapper = mappers.jtstype_to_dtype
        new_mappings = {
            'date': 'datetime64[ns]',
            'year': 'int64',
            'yearmonth': 'int64',
            'duration': 'object',
        }

        def mapper_wrapper(jtstype):
            try:
                if jtstype == 'date':
                    return new_mappings[jtstype]

                return mapper(jtstype)

            except TypeError as e:
                if jtstype in new_mappings:
                    return new_mappings[jtstype]
                else:
                    raise e

        mappers.jtstype_to_dtype = mapper_wrapper


def sanitize_schema(schema_descriptor):
    missing_type_support = False
    try:
        from jsontableschema import YearType, YearMonthType, DurationType
    except ImportError:
        missing_type_support = True

    for field in schema_descriptor.get('fields', []):
        if missing_type_support:
            # Convert unsupported types to integer and string
            # as appropriate

            type_mapping = {
                'integer': [
                    'gyear', 'year', 'gyearmonth', 'yearmonth'],
                'string': [
                    'duration'
                ]}

            for old_type, new_types in type_mapping.items():
                if field.get('type') in new_types:
                    field['type'] = old_type

        # Datapackage specs were changed along the way
        # Convert gyear and gyearmonth to year and yearmonth
        # https://github.com/frictionlessdata/specs/pull/370
        if field.get('type') in ['gyear', 'gyearmonth']:
            field['type'] = field['type'][1:]

        # Default datetime field format must match '%Y-%m-%dT%H:%M:%SZ'
        # However, data.world may fail to include 'Z' at the end
        if field['type'] == 'datetime' and 'format' not in field:
            field['format'] = 'any'


def sanitize_resource_schema(r):
    """Sanitize table schema for increased compatibility

    Up to version 0.9.0 jsontableschema did not support
    year, yearmonth and duration field types
    https://github.com/frictionlessdata/jsontableschema-py/pull/152
    """
    if 'schema' in r.descriptor:
        sanitize_schema(r.descriptor['schema'])

    return r


def align_table_fields(fields, unordered_row):
    """Ensure columns appear in the same order for every row in table"""
    fields_idx = {f: pos for pos, f in enumerate(fields)}
    return OrderedDict(sorted(unordered_row.items(),
                              key=lambda i: fields_idx[i[0]]))
