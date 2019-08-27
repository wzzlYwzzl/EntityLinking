import os
import re

# 用于提取词的m2e文件
m2e_file = "/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/test_m2e.txt"

# 存储词典的文件
dict_file = "/Users/caoxiaojie/pythonCode/EntityLinking/data/user_dict/mention_dict.txt"

# 默认的词频
default_freq = '10'

# 默认的词性
default_POS = 'n'

# 除去句子中哪些字符
re_rm = re.compile('([\"\(\)]+)')

with open(m2e_file, mode='r', encoding='utf-8') as f_read:
    with open(dict_file, mode='w+', encoding='utf-8') as f_write:
        pre_word = ''
        for line in f_read:
            fields = line.split('\t')
            if len(fields) == 2:
                word = fields[0].strip()
                if word != pre_word:
                    pre_word = word
                    f_write.write('{}\t{}\t{}\n'.format(
                        word, default_freq, default_POS))
