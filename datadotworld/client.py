import os
import urllib
import requests
import pandas as pd
from io import BytesIO

class DataDotWorld:
    """A Python Client for Accessing data.world"""

    def __init__(self, token=None):
        self.token = token

    def query(self, dataset, query, type = "sql"):
        statement = 'https://query.data.world/' + type + '/' + dataset + '?query=' + urllib.parse.quote(query)
        headers = {
                'Accept': 'text/csv', 
                'Authorization': 'Bearer ' + self.token
                }
        response = requests.get(statement, headers=headers)
        return(pd.read_csv(BytesIO(response.content)))
        #return(response.content)
