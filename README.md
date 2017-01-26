# data.world-py

A python client for querying data.world datasets.

## Install

This library hasn't yet been added to a central package repository -
you can install it using `pip` directly from this github repo:

```
pip install git+git://github.com/datadotworld/data.world-py.git
```

## Use

### Setting up the client

Once installed, you can instantiate a client by providing your
data.world API token to the constructor.  You can find your API
token at https://data.world/settings/advanced

you can either send the token in the constructor:
```
from datadotworld import DataDotWorld

client = DataDotWorld(token = "YOUR_API_TOKEN")
```

or you can insert your token into a `.data.world` file in your home
directory, and the constructor will read it from there:

```
echo 'token=YOUR_API_TOKEN' > ~/.data.world
```
then
```
from datadotworld import DataDotWorld

client = DataDotWorld()
```

### Querying

The client supports one method - `query`, which can be used to send a
`dwSQL` or a `SPARQL` query to a particular dataset's query endpoint.

`query` returns a results object which can be used to access the results
as a raw CSV string, a stream containing CSV bytes, a `csv.reader` to
read the CSV results line-by-line, or a PANDAS data frame (if you have
PANDAS installed, it is an optional dependency for this library.

```
>>> results = client.query(dataset="bryon/odin-2015-2016", query="SELECT * FROM Tables")
```
```
>>> results.as_string()
'tableId,tableName\r\nODIN-2015-2016-raw.csv/ODIN-2015-2016-raw,ODIN-2015-2016-raw\r\nODIN-2015-2016-standardized.csv/ODIN-2015-2016-standardized,ODIN-2015-2016-standardized\r\nODIN-2015-2016-weighted.csv/ODIN-2015-2016-weighted,ODIN-2015-2016-weighted\r\n'
```
```
>>> results.as_stream()
<_io.StringIO object at 0x104e899d8>
```
```
>>> for row in results.as_csv():
...   print(", ".join(row))
...
tableId, tableName
ODIN-2015-2016-raw.csv/ODIN-2015-2016-raw, ODIN-2015-2016-raw
ODIN-2015-2016-standardized.csv/ODIN-2015-2016-standardized, ODIN-2015-2016-standardized
ODIN-2015-2016-weighted.csv/ODIN-2015-2016-weighted, ODIN-2015-2016-weighted
```
```
>>> results.as_dataframe()
                                             tableId  \
0          ODIN-2015-2016-raw.csv/ODIN-2015-2016-raw
1  ODIN-2015-2016-standardized.csv/ODIN-2015-2016...
2  ODIN-2015-2016-weighted.csv/ODIN-2015-2016-wei...

                     tableName
0           ODIN-2015-2016-raw
1  ODIN-2015-2016-standardized
2      ODIN-2015-2016-weighted
```

to execute a `SPARQL` query, you need to specify the `query_type` as
`sparql`:
```
>>> df = client.query(dataset="bryon/odin-2015-2016", query='''
... PREFIX : <http://data.world/bryon/odin-2015-2016/ODIN-2015-2016-raw.csv/ODIN-2015-2016-raw#>
... PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
...
... SELECT * WHERE {
...   [ :Year ?year ; :Region ?region ; :Overall_subscore ?score ]
...   FILTER(?year = "2015")
...   } LIMIT 10''',
... query_type="sparql").as_dataframe(  )
>>> df
   year          region  score
0  2015  Eastern Africa    3.0
1  2015  Eastern Africa    2.5
2  2015  Eastern Africa    0.0
3  2015  Eastern Africa    2.0
4  2015  Western Africa   25.0
5  2015  Western Africa    3.0
6  2015  Western Africa    2.0
7  2015  Western Africa    0.5
8  2015  Western Africa    0.0
9  2015  Western Africa    0.0
```
