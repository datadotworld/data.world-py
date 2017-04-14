# data.world-py
# Copyright 2017 data.world, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
#
# This product includes software developed at
# data.world, Inc.(http://data.world/).

from __future__ import absolute_import

import functools
import re
from collections import Mapping

import collections

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

    Internally, values are of type `LazyLoadedValue`. However, clients can
    use the dictionary like they would normally use any dictionary, without
    concern for the fact that `LazyLoadedValue` instances are ``callable``.

    Parameters
    ----------
    lazy_loaded_items : dict
        Mapping of keys to values of type `LazyLoadedValue`
    """

    def __init__(self, lazy_loaded_items):
        self._dict = lazy_loaded_items

    @classmethod
    def from_keys(cls, keys, loader_func, type_hint=None):
        """Factory method for `LazyLoadedDict`

        Accepts a ``loader_func`` that is to be applied to all ``keys``.

        Parameters
        ----------
        keys : iterable
            List of keys to create the dictionary with
        loader_func : function
            Function to be applied to all keys
        type_hint : str
            Expected type of lazy loaded values.
            Used by `LazyLoadedValue`.

        Returns
        -------
        LazyLoadedDict
            A properly constructed lazy loaded dictionary

        """
        return cls({k: LazyLoadedValue(
            lambda k=k: loader_func(k), type_hint=type_hint) for k in keys})

    def __getitem__(self, item):
        return self._dict[item]()

    def __iter__(self):
        return iter(self._dict.keys())

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self._dict))

    def __str__(self):
        return str(self._dict)


class LazyLoadedValue(object):
    def __init__(self, loader_func, type_hint=None):
        self._loader_func = loader_func
        self._type_hint = type_hint

    def __call__(self, *args, **kwargs):
        return self._loader_func()

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ('<{}>'.format(self._type_hint)
             if self._type_hint is not None else repr(self._loader_func)))

    def __str__(self):
        return str(self())


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, key_mapper=None):
        self.key_mapper = key_mapper
        self.cache = {}

    def __call__(self, func):
        def wrapper(*args):
            key = self.key_mapper(*args) or args
            if not isinstance(key, collections.Hashable):
                # uncacheable. a list, for instance.
                # better to not cache than blow up.
                return func(*args)
            if key in self.cache:
                return self.cache[key]
            else:
                value = func(*args)
                self.cache[key] = value
                return value
        return wrapper

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
