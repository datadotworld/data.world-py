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

from os import environ

# define constants for the various hosts the SDK may need to connect to
# for connecting to the public data.world server, the defaults are fine -
# to connect to a separate data.world environment, the environment variables
# can be specified.
API_HOST = environ.get('DW_API_HOST', 'https://api.data.world')
DOWNLOAD_HOST = environ.get('DW_DOWNLOAD_HOST', 'https://download.data.world')
QUERY_HOST = environ.get('DW_QUERY_HOST', 'https://query.data.world')
