'''
data.world-py
Copyright 2016 data.world, Inc.

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
'''
from setuptools import setup

setup(  name='datadotworld',
        version='0.1',
        description='Python client library for data.world',
        url='http://github.com/datadotworld/data.world-py',
        author='data.world',
        author_email='help@data.world',
        license='Apache 2.0',
        packages=['datadotworld'],
        install_requires=['pandas'],
        zip_safe=False)
