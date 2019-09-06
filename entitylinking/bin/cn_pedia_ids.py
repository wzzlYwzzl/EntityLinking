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
                        

cndbpedia_file = "/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/test.txt"
id_file = "/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/id.txt"

if __name__ == '__main__':
    id_cn_dbpedia(cndbpedia_file, id_file)
