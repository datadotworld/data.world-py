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

import re
from os import path

from setuptools import setup


def read(*paths):
    filename = path.join(path.abspath(path.dirname(__file__)), *paths)
    with open(filename) as f:
        return f.read()


def find_version(*paths):
    contents = read(*paths)
    match = re.search(r'^__version__ = [\'"]([^\'"]+)[\'"]', contents, re.M)
    if not match:
        raise RuntimeError('Unable to find version string.')
    return match.group(1)


setup(
    name='datadotworld',
    version=find_version('datadotworld', '__init__.py'),
    description='Python client library for data.world',
    long_description=read('README.md'),
    url='http://github.com/datadotworld/data.world-py',
    author='data.world',
    author_email='help@data.world',
    license='Apache 2.0',
    packages=['datadotworld'],
    install_requires=[
        'requests>=2.9.2', 'urllib3 >= 1.15', 'six >= 1.10', 'certifi', 'python-dateutil'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    extras_require={
        'PANDAS': ['pandas']
    }
)
