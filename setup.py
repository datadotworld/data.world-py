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
    keywords='data.world dataset',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'certifi>=2017.04.17',
        'click>=6.0,<7.0a',
        'configparser>=3.5.0,<4.0a',
        'datapackage>=1.6.2,<2.0a',
        'tableschema>=1.5.2,<2.0a',
        'python-dateutil>=2.6.0,<3.0a',
        'requests>=2.0.0,<3.0a',
        'six>=1.5.0,<2.0a',
        'tabulator>=1.22.0',
        'urllib3>=1.15,<2.0a',
    ],
    setup_requires=[
        'pytest-runner>=2.11,<3.0a',
    ],
    tests_require=[
        'coverage>=4.4.2,<=4.5.3',
        'doublex>=1.8.4,<2.0a',
        'flake8>=2.6.0,<=3.7.7',
        'numpy<=1.16.4',
        'pandas<0.25',
        'pyhamcrest>=1.9.0,<2.0a',
        'pytest>=4.6.3,<5.0a',
        'responses>=0.5.1,<1.0a',
    ],
    extras_require={
        'pandas': [
            'numpy<=1.16.4',
            'pandas<0.25',
        ],
    },
    entry_points={
        'console_scripts': [
            'dw=datadotworld.cli:cli',
        ],
    },
)
