# encoding=utf-8
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from entitylinking.index_elasticsearch.triple_index_creator import triple_index_create

if __name__ == '__main__':
    data = '/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/test.txt'
    indexname = 'triple'
    triple_index_create(indexname, data, True)