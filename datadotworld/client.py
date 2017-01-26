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

import os
import re
import requests
import csv
from io import StringIO


class DataDotWorld:
    """A Python Client for Accessing data.world"""

    def __init__(self, token=None, propsfile="~/.data.world",
                 protocol="https",
                 queryHost="query.data.world"):
        regex = re.compile(r"^token\s*=\s*(\S.*)$")
        filename = os.path.expanduser(propsfile)
        self.token = token
        if self.token is None and os.path.isfile(filename):
            with open(filename, 'r') as props:
                self.token = next(iter([regex.match(line.strip()).group(1) for line in props if regex.match(line)]),
                                  None)
        if self.token is None:
            raise RuntimeError((
                'you must either provide an API token to this constructor, or create a '
                '.data.world file in your home directory with your API token'))
        self.protocol = protocol
        self.queryHost = queryHost

    class Results:
        def __init__(self, raw):
            self.raw = raw

        def __unicode__(self):
            return self.as_string()

        def __repr__(self):
            return "{0}\n...".format(self.as_string()[:250])

        def as_string(self):
            return self.raw

        def as_stream(self):
            return StringIO(self.raw)

        def as_dataframe(self):
            try:
                import pandas as pd
            except ImportError:
                raise RuntimeError("You need to have pandas installed to use .asDf()")
            else:
                return pd.read_csv(self.as_stream())

        def as_csv(self):
            # TODO: support UTF-8 formatted CSV in Python 2.x
            return csv.reader(self.as_stream())

    def query(self, dataset, query, query_type="sql"):
        from . import __version__
        # TODO: set useragent
        params = {
            "query": query
        }
        url = "{0}://{1}/{2}/{3}".format(self.protocol,
                                         self.queryHost,
                                         query_type,
                                         dataset)
        headers = {
            'User-Agent': 'data.world-py - {0}'.format(__version__),
            'Accept': 'text/csv',
            'Authorization': 'Bearer {0}'.format(self.token)
        }
        print headers
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return DataDotWorld.Results(response.text)
        raise RuntimeError('error running query.')
