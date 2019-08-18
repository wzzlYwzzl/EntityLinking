import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from entitylinking.config.app_config import AppConfig

if __name__ == '__main__':
    config_file = '/Users/caoxiaojie/pythonCode/EntityLinking/data/config.ini'
    AppConfig.init_instance(config_file)
    print(AppConfig.instance().index_dir)
