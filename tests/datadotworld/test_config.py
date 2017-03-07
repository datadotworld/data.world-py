import configparser
import pytest

from os import path
from datadotworld.config import Config


class TestConfig:

    # Fixtures

    @pytest.fixture()
    def config_file_path(self, tmpdir):
        return str(tmpdir.join('.datadotworld'))

    @pytest.fixture()
    def legacy_file_path(self, tmpdir):
        return str(tmpdir.join('.data.world'))

    @pytest.fixture()
    def default_config_file(self, config_file_path):
        config_parser = configparser.ConfigParser()
        config_parser['default'] = {'auth_token': 'abcd'}
        config_parser.write(open(config_file_path, 'w+'))

    @pytest.fixture()
    def alternative_config_file(self, config_file_path):
        config_parser = configparser.ConfigParser()
        config_parser['alternative'] = {'auth_token': 'alternativeabcd'}
        config_parser.write(open(config_file_path, 'w+'))

    @pytest.fixture()
    def legacy_config_file(self, legacy_file_path):
        with open(legacy_file_path, 'w+') as legacy_file:
            legacy_file.write("token=legacyabcd")

    # Tests

    @pytest.mark.usefixtures('default_config_file')
    def test_auth_token(self, config_file_path):
        config = Config(config_file_path=config_file_path)
        assert config.auth_token == 'abcd'

    @pytest.mark.usefixtures('alternative_config_file')
    def test_alternative_token(self, config_file_path):
        config = Config(profile='alternative', config_file_path=config_file_path)
        assert config.auth_token == 'alternativeabcd'

    @pytest.mark.usefixtures('legacy_config_file')
    def test_legacy_token(self, legacy_file_path, config_file_path):
        assert not path.isfile(config_file_path)
        config = Config(legacy_file_path=legacy_file_path, config_file_path=config_file_path)
        assert config.auth_token == 'legacyabcd'
        assert path.isfile(config_file_path)
