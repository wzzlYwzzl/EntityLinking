# encoding=utf-8
import sys

sys.path.append('/Users/caoxiaojie/pythonCode/EntityLinking')


def create_index_without_id(indexname, data):
    """创建没有id的三元组索引
    """
    from entitylinking.index_elasticsearch.triple_index_creator import triple_index_create
    triple_index_create(indexname, data, True)


def create_index_with_id(indexname, data, id_file):
    from entitylinking.index_elasticsearch.triple_index_with_id_creator import triple_index_create
    triple_index_create(indexname, id_file, data, True)


if __name__ == '__main__':
    data = '/Users/caoxiaojie/pythonCode/EntityLinking/data/text_dir'
    indexname = 'triple_id'
    id_file = '/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/id.txt'
    create_index_with_id(indexname, data, id_file)
