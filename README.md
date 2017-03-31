# data.world-py

A python library for working with data.world datasets

## Quick start

### Install

This library hasn't yet been added to a central package repository -
you can install it using `pip` directly from this github repo:

```
pip install git+git://github.com/datadotworld/data.world-py.git
```

### Configure

Before you start using the library, you must first set it up with your access token.  
To do that, run the following command:
```bash
dw configure
```

Your API token can be obtained on data.world under [Settings > Advanced](https://data.world/settings/advanced)

### Load a dataset

The `load_dataset()` function facilitates maintaining copies of datasets on the local filesystem. 
It will download a given dataset's [datapackage](http://specs.frictionlessdata.io/data-package/) 
and store it under `~/.dw/cache`. When used subsequently, `load_dataset()` will use the copy stored on disk and will
work offline, unless it's called with `force_update=True`.

Once loaded, a dataset (data and metadata) can be conveniently accessed via the object returned by `load_dataset()`.

Start by importing the `datadotworld` module:
```python
import datadotworld as dw
```

Then, invoke the `load_dataset` function, to download a dataset and work with it locally.  
For example:
```python
intro_dataset = dw.load_dataset('jonloyens/an-intro-to-dataworld-dataset')
```

Dataset objects allow access to data via three different properties `raw_data`, `tables` and `dataframes`.
Each of these properties is a mapping (dict) whose values are of type `bytes`, `list` and `pandas.DataFrame`, 
respectively. Values are lazy loaded and cached once loaded. Their keys are the names of the files 
contained in the dataset.

For example:
```python
>>> intro_dataset.dataframes
LazyLoadedDict({
    'changelog': LazyLoadedValue(<pandas.DataFrame>), 
    'datadotworldbballstats': LazyLoadedValue(<pandas.DataFrame>), 
    'datadotworldbballteam': LazyLoadedValue(<pandas.DataFrame>)})
```

**IMPORTANT**: Not all files in a dataset are tabular, therefore some will be exposed via `raw_data` only.

Tables are lists of rows, each represented by a mapping (dict) of column names to their respective values.

For example:
```python
>>> stats_table = intro_dataset.tables['datadotworldbballstats']
>>> stats_table[0]
OrderedDict([('Name', 'Jon'),
             ('PointsPerGame', Decimal('20.4')),
             ('AssistsPerGame', Decimal('1.3'))])
```

You can also review the metadata associated with a file or the entire dataset, using the `describe` function.  
For example:
```python
>>> intro_dataset.describe()
{'homepage': 'https://data.world/jonloyens/an-intro-to-dataworld-dataset',
 'name': 'jonloyens_an-intro-to-dataworld-dataset',
 'resources': [{'format': 'csv',
   'name': 'changelog',
   'path': 'data/ChangeLog.csv'},
  {'format': 'csv',
   'name': 'datadotworldbballstats',
   'path': 'data/DataDotWorldBBallStats.csv'},
  {'format': 'csv',
   'name': 'datadotworldbballteam',
   'path': 'data/DataDotWorldBBallTeam.csv'}]}


>>> intro_dataset.describe('datadotworldbballstats')
{'format': 'csv',
 'name': 'datadotworldbballstats',
 'path': 'data/DataDotWorldBBallStats.csv',
 'schema': {'fields': [{'name': 'Name', 'title': 'Name', 'type': 'string'},
                       {'name': 'PointsPerGame',
                        'title': 'PointsPerGame',
                        'type': 'number'},
                       {'name': 'AssistsPerGame',
                        'title': 'AssistsPerGame',
                        'type': 'number'}]}}
```

### Query a dataset

The 'query()' function allows datasets to be queried live using `SQL` or `SPARQL` query languages.

To query a dataset, invoke the `query` function.
For example:
```python
results = dw.query('jonloyens/an-intro-to-dataworld-dataset', 'SELECT * FROM DataDotWorldBBallStats')
```

Query result objects allow access to the data via `raw_data`, `table` and `dataframe` properties, of type `json`, `list`
and `pandas.DataFrame`, respectively.

For example:
```python
>>> results.dataframe
      Name  PointsPerGame  AssistsPerGame
0      Jon           20.4             1.3
1      Rob           15.5             8.0
2   Sharon           30.1            11.2
3     Alex            8.2             0.5
4  Rebecca           12.3            17.0
5   Ariane           18.1             3.0
6    Bryon           16.0             8.5
7     Matt           13.0             2.1
```

Tables are lists of rows, each represented by a mapping (dict) of column names to their respective values.
For example:
```python
>>> results.table[0]
OrderedDict([('Name', 'Jon'),
             ('PointsPerGame', Decimal('20.4')),
             ('AssistsPerGame', Decimal('1.3'))])
```

To query using `SPARQL` invoke `query()` using `query_type='sparql'`, or else, it will assume 
the query to be a `SQL` query.

Just like in the dataset case, you can view the metadata associated with a query result using the `describe()` function.
For example:
```python
>>> results.describe()
{'fields': [{'name': 'Name', 'type': 'string'},
            {'name': 'PointsPerGame', 'type': 'number'},
            {'name': 'AssistsPerGame', 'type': 'number'}]}
```

### Create and update datasets

To create and update datasets, start by calling the `api_client` function.
For example:
```python
client = dw.api_client()
```
The client supports various methods for creating and updating datasets and dataset files:

- `create_dataset`
- `update_dataset`
- `replace_dataset`
- `get_dataset`
- `add_files_via_url`
- `sync_files`
- `upload_files`
- `delete_files`

You can find more about those functions using `help()`

