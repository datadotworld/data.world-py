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

import re

DATASET_KEY_PATTERN = re.compile('^(?:https?://[^/]+/)?([a-z0-9-]+)/([a-z0-9-]+)$')  # Recognizes URLs and paths


def parse_dataset_key(dataset_key):
    """Parse a dataset URL or path and return the owner and the dataset id

    Parameters
    ----------
    dataset_key : str
        Dataset key (in the form of owner/id) or dataset URL

    Returns
    -------
    dataset_owner
        User name of the dataset owner
    dataset_id
        ID of the dataset

    Raises
    ------
    ValueError
        If the provided key does comply to the expected pattern

    Examples
    --------
    >>> util.parse_dataset_key('https://data.world/jonloyens/an-intro-to-datadotworld-dataset')
    ('jonloyens', 'an-intro-to-datadotworld-dataset')
    >>> util.parse_dataset_key('jonloyens/an-intro-to-datadotworld-dataset')
    ('jonloyens', 'an-intro-to-datadotworld-dataset')
    """
    match = re.match(DATASET_KEY_PATTERN, dataset_key)
    if not match:
        raise ValueError('Invalid dataset key. Key must include user and dataset names, separated by / '
                         '(i.e. user/dataset).')
    return match.groups()


def _user_agent():
    from datadotworld import __version__
    return 'data.world-py - {}'.format(__version__)
