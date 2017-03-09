import sys

import pytest
from click.testing import CliRunner
from doublex import Spy, assert_that, called, property_set

from datadotworld import cli
from datadotworld.config import Config


@pytest.mark.skipif(sys.version_info >= (3, 0),
                    reason="See: http://click.pocoo.org/5/python3/#python-3-surrogate-handling")
def test_configure():
    runner = CliRunner()
    config = Spy(Config)

    runner.invoke(cli.configure, input='token\n', obj={'config': config})

    assert_that(config, property_set('auth_token').to('token'))
    assert_that(config.save, called())
