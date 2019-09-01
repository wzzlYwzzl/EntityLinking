# encoding=utf-8
import sys

sys.path.append('/Users/caoxiaojie/pythonCode/EntityLinking')

from entitylinking.index_elasticsearch.triple_index_creator import triple_index_create

if __name__ == '__main__':
    data = '/Users/caoxiaojie/pythonCode/EntityLinking/data/text_dir'
    indexname = 'triple'
    triple_index_create(indexname, data, True)