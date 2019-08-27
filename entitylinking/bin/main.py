import sys

sys.path.append('/Users/caoxiaojie/pythonCode/EntityLinking')

from entitylinking.config.app_config import AppConfig
from entitylinking.algorithm.agdistis import Agdistis
from entitylinking.base.document import Document

config_file = '/Users/caoxiaojie/pythonCode/EntityLinking/data/config.ini'


def print_doc(doc):
    for mention in doc.mention_list:
        for cand in mention.candidates:
            print(cand.entity, " : ", cand.score)
        print('------------------------------')


if __name__ == '__main__':
    AppConfig.init_instance(config_file)
    agdistis = Agdistis()
    '''
    doc = Document('打球的<entity>李娜</entity>和唱歌的<entity>李娜</entity>')
    ret_doc = agdistis.run(doc)
    print_doc(ret_doc)

    print('======================================')

    doc = Document('<entity>李娜</entity>的老公是<entity>姜山</entity>')
    ret_doc = agdistis.run(doc)
    print_doc(ret_doc)

    print('======================================')
    '''

    doc = Document('唱歌的<entity>李娜</entity>是谁')
    ret_doc = agdistis.run(doc)
    print_doc(ret_doc)
