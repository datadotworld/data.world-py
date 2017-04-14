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

import re
from os import path

from setuptools import setup, find_packages


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
    description='Python library for data.world',
    long_description=read('README.rst'),
    url='http://github.com/datadotworld/data.world-py',
    author='data.world',
    author_email='help@data.world',
    license='Apache 2.0',
    packages=find_packages(),
    keywords=[
        'data.world',
        'dataset',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'certifi',
        'click',
        'configparser',
        'datapackage>=0.8.8,<1.0a',
        'jsontableschema>=0.10.0,<1.0a',
        'python-dateutil',
        'requests',
        'six',
        'tabulator',
        'urllib3',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'doublex',
        'pyhamcrest',
        'responses',
        'pytest',
        'jsontableschema_pandas>=0.3.0,<1.0a',
        'pandas<0.19a',
    ],
    extras_require={
        'PANDAS': [
            'jsontableschema_pandas>=0.3.0,<1.0a',
            'pandas<0.19a',
        ],
    },
    entry_points={
        'console_scripts': [
            'dw=datadotworld.cli:cli',
        ],
    },
)
