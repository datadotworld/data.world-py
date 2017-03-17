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

Start by importing the `datadotworld` module:
```python
import datadotworld as dw
```

Then, invoke the `load_dataset` function, to download a dataset and work with it locally.  
For example:
```python
intro_dataset = dw.load_dataset('jonloyens/an-intro-to-dataworld-dataset')
```

Dataset objects allow access to data in 3 different ways, via `raw_data`, `tables` and `dataframes` properties.  
For example:
```python
>>> list(intro_dataset.dataframes)
['datadotworldbballteam', 'datadotworldbballstats', 'anintrotodata.worlddatasetchangelog-sheet1']
```

**IMPORTANT**: Not all files in a dataset are tabular, therefore some will be exposed via `raw_data` only.

You can also review the metadata associated with a file or the entire dataset, using the `describe` function.  
For example:
```python
>>> intro_dataset.describe('datadotworldbballteam')
{'format': 'csv',
 'name': 'datadotworldbballteam',
 'path': 'data/DataDotWorldBBallTeam.csv',
 'schema': {'fields': [{'name': 'Name', 'title': 'Name', 'type': 'string'},
                       {'name': 'Height', 'title': 'Height', 'type': 'string'},
                       {'name': 'Handedness',
                        'title': 'Handedness',
                        'type': 'string'}]}}

```

### Query a dataset

To query a dataset, invoke the `query` function.
For example:
```python
results = dw.query('jonloyens/an-intro-to-dataworld-dataset', 'SELECT * FROM DataDotWorldBBallStats')
```

Query result objects allow access to the data via `raw_data`, `table` and `dataframe` properties.
For example:
```python
>>> list(results.table)
[{'AssistsPerGame': '1.3', 'Name': 'Jon', 'PointsPerGame': '20.4'},
 {'AssistsPerGame': '8', 'Name': 'Rob', 'PointsPerGame': '15.5'},
 {'AssistsPerGame': '11.2', 'Name': 'Sharon', 'PointsPerGame': '30.1'},
 {'AssistsPerGame': '0.5', 'Name': 'Alex', 'PointsPerGame': '8.2'},
 {'AssistsPerGame': '17', 'Name': 'Rebecca', 'PointsPerGame': '12.3'},
 {'AssistsPerGame': '3', 'Name': 'Ariane', 'PointsPerGame': '18.1'},
 {'AssistsPerGame': '8.5', 'Name': 'Bryon', 'PointsPerGame': '16'},
 {'AssistsPerGame': '2.1', 'Name': 'Matt', 'PointsPerGame': '13'}]
```

Queries can be written in SQL or SPARQL. Call the query function using `query_type='sparql'`, or else, it will assume 
the query to be a SQL query.

### Create and update datasets

To create and update datasets, start by calling the `api_client` function.
For example:
```python
client = dw.api_client()
```
The client supports various methods for creating and updating datasets and dataset files:

- `create_dataset`
- `patch_dataset`
- `replace_dataset`
- `get_dataset`
- `add_files_via_url`
- `sync_files`
- `upload_files`
- `delete_files`

You can find more about those functions using `help()`

