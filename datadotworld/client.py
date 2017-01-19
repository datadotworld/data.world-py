import os
import re
import urllib
import requests
import pandas as pd
from io import BytesIO

class DataDotWorld:
    """A Python Client for Accessing data.world"""

    def __init__(self, token=None, propsfile="~/.data.world"):
        regex = re.compile(r"^token\s*=\s*(\S.*)$")
        filename = os.path.expanduser("~/.data.world")
        self.token = token
        if self.token == None and os.path.isfile(filename):
            with open(filename, 'r') as propsfile:
                self.token = next(iter([regex.match(line.strip()).group(1) for line in propsfile if regex.match(line)]), None)
        if self.token == None:
            raise RuntimeError(('you must either provide an API token to this constructor, or create a '
                    '.data.world file in your home directory with your API token'))

    def query(self, dataset, query, type = "sql"):
        statement = 'https://query.data.world/' + type + '/' + dataset + '?query=' + urllib.parse.quote(query)
        headers = {
                'Accept': 'text/csv', 
                'Authorization': 'Bearer ' + self.token
                }
        response = requests.get(statement, headers=headers)
        if response.status_code == 200:
            return(pd.read_csv(BytesIO(response.content)))
        raise RuntimeError('error running query.')
