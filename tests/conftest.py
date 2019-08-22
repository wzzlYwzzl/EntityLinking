import pytest
from os.path import join, dirname

from entitylinking.config.app_config import AppConfig
from entitylinking.index_whoosh.triple_index import TripleIndex

config_file = join(dirname(dirname(__file__)), 'data/config.ini')

@pytest.fixture(scope="session")
def config_instance():
    AppConfig.init_instance(config_file)
    return AppConfig.instance()

@pytest.fixture(scope="session")
def triple_index(config_instance):
    index_dir = config_instance.index_dir
    return TripleIndex(index_dir)