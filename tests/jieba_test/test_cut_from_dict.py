#encoding=utf-8
from __future__ import print_function
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from entitylinking.jieba import Tokenizer


if __name__ == '__main__':
    token = Tokenizer(dictionary='/Users/caoxiaojie/pythonCode/EntityLinking/data/user_dict/mention_dict.txt', split='\t')
    words = token.cut_from_dict('李娜英是网球李娜')
    for word,start,end in words:
        print(word, start, end)