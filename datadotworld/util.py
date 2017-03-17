"""
data.world-py
Copyright 2017 data.world, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the
License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.

This product includes software developed at
data.world, Inc.(http://www.data.world/).
"""
from __future__ import absolute_import

import re
from collections import Mapping

DATASET_KEY_PATTERN = re.compile(
    '^(?:https?://[^/]+/)?([a-z0-9-]+)/([a-z0-9-]+)$')  # URLs and paths


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
    >>> from datadotworld import util
    >>> util.parse_dataset_key(
    ...     'https://data.world/jonloyens/an-intro-to-datadotworld-dataset')
    ('jonloyens', 'an-intro-to-datadotworld-dataset')
    >>> util.parse_dataset_key('jonloyens/an-intro-to-datadotworld-dataset')
    ('jonloyens', 'an-intro-to-datadotworld-dataset')
    """
    match = re.match(DATASET_KEY_PATTERN, dataset_key)
    if not match:
        raise ValueError('Invalid dataset key. Key must include user and '
                         'dataset names, separated by (i.e. user/dataset).')
    return match.groups()


def _user_agent():
    from datadotworld import __version__
    return 'data.world-py - {}'.format(__version__)


class LazyLoadedDict(Mapping):
    """Custom immutable dict implementation with lazy loaded values

    Parameters
    ----------
    keys : iterable
        Dictionary keys
    loader_func : function
        Function used to instantiate/load the value for a given key, on demand
    type_hint : str
        String describing the type of the lazy loaded value. Used in place of
        the value before value is loaded.
    """

    def __init__(self, keys, loader_func, type_hint='unknown'):
        self._keys = keys
        self._loader_func = loader_func
        self._type_hint = type_hint
        self.__cache = {}  # Would love for this to be a weak ref dict

    def __getitem__(self, item):
        if item in self._keys and item not in self.__cache:
            self.__cache[item] = self._loader_func(item)
        return self.__cache[item]

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)

    def __repr__(self):
        fully_qualified_type = '{}.{}'.format(
            self.__module__, self.__class__.__name__)
        return '<{} with values of type: {}>'.format(
            fully_qualified_type, self._type_hint)

    def __str__(self):
        def value_or_placeholder(key):
            if key in self.__cache:
                return repr(self.__cache[key])
            else:
                return '<{}>'.format(self._type_hint)

        key_value_strings = ['{}: {}'.format(repr(k), value_or_placeholder(k))
                             for k in self._keys]
        return '{{{}}}'.format(', '.join(key_value_strings))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
