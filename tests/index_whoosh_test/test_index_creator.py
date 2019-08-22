import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from entitylinking.index_whoosh.triple_index_creator import triple_index_create


def create_test_data_file(test_data, start_index, count):
    data = '/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/baike_triples.txt'
    if os.path.exists(test_data):
        return

    with open(test_data, mode='w+', encoding='utf8') as f_in:
        with open(data, mode='r', encoding='utf8') as f:
            tmp = 0
            for line in f:
                tmp += 1
                if tmp < start_index:
                    continue
                elif tmp - start_index > count:
                    break
                else:
                    f_in.write(line)



@pytest.mark.index_creator_new
def test_index_creator():
    index_dir = '/Users/caoxiaojie/pythonCode/EntityLinking/data/index_new'
    test_data = '/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/test.txt'
    create_test_data_file(test_data, 1, 1000000)
    triple_index_create(test_data, index_dir)
    assert True
