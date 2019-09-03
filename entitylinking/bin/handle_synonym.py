# 原始要加工的文件
file_synonym = "/Users/caoxiaojie/pythonCode/EntityLinking/tools/elasticsearch/elasticsearch-jieba-plugin-7.3.1/dic/synonyms.txt"

# 要得到的文件
file_out = "/Users/caoxiaojie/pythonCode/EntityLinking/tools/elasticsearch/elasticsearch-jieba-plugin-7.3.1/dic/out.txt"


def handle_synonym(file_in, file_out):
    with open(file_in, mode='r', encoding='utf-8') as f:
        with open(file_out, mode='w+', encoding='utf-8') as f_out:
            for line in f:
                if '=' in line:
                    fields = line.split('=')
                    if len(fields) >= 2:
                        words = fields[1].strip()
                        if words:
                            words = ','.join(words.split(' '))
                            f_out.write(words)
                            f_out.write('\n')


def create_synonym_dict(file_in, file_out):
    word_set = set()
    with open(file_in, mode='r', encoding='utf-8') as f:
        with open(file_out, mode='w+', encoding='utf-8') as f_out:
            for line in f:
                fields = line.split(',')
                for field in fields:
                    word = field.strip()
                    if word and word not in word_set:
                        word_set.add(word)
                        f_out.write('{} 10\n'.format(word))

if __name__ == '__main__':
    create_synonym_dict(file_synonym, file_out)