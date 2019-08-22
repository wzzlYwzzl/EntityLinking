import sys

sys.path.append('/Users/caoxiaojie/pythonCode/EntityLinking')

from entitylinking.base.document import Document
from entitylinking.algorithm.agdistis import Agdistis
from entitylinking.config.app_config import AppConfig


config_file = '/Users/caoxiaojie/pythonCode/EntityLinking/data/config.ini'


if __name__ == '__main__':
    AppConfig.init_instance(config_file)
    agdistis = Agdistis()
    doc = Document('<entity>李娜</entity>的丈夫是<entity>姜山</entity>')
    agdistis.run(doc)
