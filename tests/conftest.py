import pytest
from os.path import join, dirname

from entitylinking.config.app_config import AppConfig
from entitylinking.index.triple_index import TripleIndex

config_file = join(dirname(dirname(__file__)), 'data/config.txt')

@pytest.fixture(scope="session")
def config_instance():
    AppConfig.init_instance(config_file)
    return AppConfig.instance()

@pytest.fixture(scope="session")
def triple_index():
    return TripleIndex()
