def duplicate_remove(stopwords, new_stopwords):
    """stopwords去重
    """
    word_set = set()
    with open(stopwords, mode='r', encoding='utf-8') as f_in:
        with open(new_stopwords, mode='w+', encoding='utf-8') as f_out:
            for line in f_in:
                word = line.strip()
                if word not in word_set:
                    f_out.write('{}\n'.format(word))
                    word_set.add(word)


if __name__ == '__main__':
    stopwords = '/Users/caoxiaojie/pythonCode/EntityLinking/data/user_dict/stopwords.txt'
    new_stopwords = '/Users/caoxiaojie/pythonCode/EntityLinking/data/user_dict/stopwords_new.txt'
    duplicate_remove(stopwords, new_stopwords)