#encoding=utf-8
from __future__ import print_function
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from entitylinking.ner.dict_ner import DictNER


if __name__ == '__main__':
    ner = DictNER('/Users/caoxiaojie/pythonCode/EntityLinking/data/user_dict/mention_dict.txt')
    mentions = ner.get_mentions('李娜英是网球李娜')
    for mention in mentions:
        print(mention.word, mention.start_pos, mention.end_pos)