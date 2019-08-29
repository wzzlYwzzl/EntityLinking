import sys

sys.path.append('/Users/caoxiaojie/pythonCode/EntityLinking')

from entitylinking.index_whoosh.triple_index_creator import triple_index_create

if __name__ == '__main__':
    data = '/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/test.txt'
    index_dir = '/Users/caoxiaojie/pythonCode/EntityLinking/data/index_all'
    triple_index_create(data, index_dir)
    sys.exit(0)
