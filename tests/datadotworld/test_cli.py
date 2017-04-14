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

import sys

import pytest
from click.testing import CliRunner
from doublex import Spy, assert_that, called, property_set

from datadotworld import cli
from datadotworld.config import Config


@pytest.mark.skipif(
    sys.version_info >= (3, 0),
    reason="http://click.pocoo.org/5/python3/#python-3-surrogate-handling")
def test_configure():
    runner = CliRunner()
    config = Spy(Config)

    runner.invoke(cli.configure, input='token\n', obj={'config': config})

    assert_that(config, property_set('auth_token').to('token'))
    assert_that(config.save, called())
