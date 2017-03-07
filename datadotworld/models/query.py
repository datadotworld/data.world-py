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
from __future__ import absolute_import

import csv
from io import StringIO


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
