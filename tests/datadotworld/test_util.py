from doublex import assert_that
from hamcrest import equal_to, calling, raises

from datadotworld import util


def test_parse_dataset_key():
    path_owner, path_id = util.parse_dataset_key('owner/dataset')
    assert_that(path_owner, equal_to('owner'))
    assert_that(path_id, equal_to('dataset'))


def test_parse_dataset_key_with_url():
    url_owner, url_id = util.parse_dataset_key('https://data.world/owner/dataset')
    assert_that(url_owner, equal_to('owner'))
    assert_that(url_id, equal_to('dataset'))


def test_parse_dataset_key_with_bad_path():
    assert_that(calling(util.parse_dataset_key).with_args('owner/dataset/somethingelse'), raises(ValueError))


def test_parse_dataset_key_with_bad_url():
    assert_that(calling(util.parse_dataset_key).with_args('ftp://data.world/owner/dataset'), raises(ValueError))


def test__user_agent():
    from datadotworld import __version__
    assert_that(util._user_agent(), equal_to('data.world-py - {}'.format(__version__)))
