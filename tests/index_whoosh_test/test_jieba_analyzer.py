import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from entitylinking.index_whoosh.jieba_analyzer import ChineseAnalyzer
import entitylinking.jieba as jieba

user_dict = '/Users/caoxiaojie/pythonCode/EntityLinking/data/user_dict/dict.txt'
jieba.load_userdict(user_dict)
analyzer = ChineseAnalyzer()
ret = analyzer('<a>姜山（著名网球教练员）</a>')

print(ret)