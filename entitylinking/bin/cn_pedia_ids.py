"""将cn-pedia的数据id化，也就是为SPO三元组的S添加唯一ID。
"""


def id_cn_dbpedia(cn_pedia_file, id_file):
    """
    """
    id_dict = {}
    subject_id = 0
    with open(cn_pedia_file, mode='r', encoding='utf-8') as f_in:
        with open(id_file, mode='w+', encoding='utf-8') as f_out:
            for line in f_in:
                fields = line.split('\t')
                subject = fields[0].strip()
                if subject:
                    if subject not in id_dict:
                        subject_id += 1
                        id_dict[subject] = subject_id
                        f_out.write('{}\t{}\n'.format(subject, subject_id))


def load_id_file(id_file):
    """加载id文件
    """
    id_dict = {}
    with open(id_file, mode='r', encoding='utf-8') as f:
        for line in f:
            fields = line.split('\t')
            id_dict[fields[0]] = fields[1]

    return id_dict


def mention2id(mention_file, id_file, mention_out):
    """将menton2e.txt文件中的内容也转换为id
    """
    id_dict = load_id_file(id_file)
    with open(mention_file, mode='r', encoding='utf-8') as f:
        with open(mention_out, mode='w+', encoding='utf-8') as f_out:
            for line in f:
                fields = line.split('\t')
                mention = fields[0].strip()
                entity = fields[1].strip()
                if entity in id_dict:
                    f_out.write('{}\t{}\n'.format(mention, id_dict[entity]))
                else:
                    f_out.write('{}\tNULL\n'.format(mention))


cndbpedia_file = "/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/test.txt"
id_file = "/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/id.txt"
m2e = "/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/m2e.txt"
m2id = "/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/m2id.txt"

if __name__ == '__main__':
    #id_cn_dbpedia(cndbpedia_file, id_file)
    mention2id(m2e, id_file, m2id)