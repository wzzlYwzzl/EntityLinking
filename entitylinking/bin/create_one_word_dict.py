def create_dict(text_file, out_file):
    char_set = set()
    count = 0
    with open(text_file, mode='r', encoding='utf-8') as f:
        with open(out_file, mode='w+', encoding='utf-8') as f_in:
            for line in f:
                count += 1
                for ch in line:
                    if '\u4e00' <= ch <= '\u9fff':
                        if ch in char_set:
                            continue
                        else:
                            char_set.add(ch)
                            f_in.write('{} 10\n'.format(ch))
                if count % 100000 == 0:
                    print("完成了：{}行".format(count))


if __name__ == '__main__':
    text = '/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/baike_dict.txt'
    out_file = '/Users/caoxiaojie/pythonCode/EntityLinking/data/cn-pedia/baike_dict2.txt'
    create_dict(text, out_file)
