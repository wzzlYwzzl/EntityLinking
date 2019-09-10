import sys
sys.path.append('/Users/caoxiaojie/pythonCode/EntityLinking')

import json

from entitylinking.base.document import Document
from entitylinking.algorithm.agdistis import Agdistis
from entitylinking.config.app_config import AppConfig
from entitylinking.log.log_manager import LogManager

config_file = '/Users/caoxiaojie/pythonCode/EntityLinking/data/config_test.ini'


def print_doc(doc):
    for mention in doc.mention_list:
        for cand in mention.candidates:
            print(cand.entity, cand.id, " : ", cand.score)
        print('------------------------------')


def print_info(doc, text_json):
    """打印基本信息
    """
    log_printer = LogManager.instance()
    log_printer.info(text_json['text'])
    for t_m in text_json['mention_data']:
        mention = t_m['mention']
        offset = t_m['offset']
        kb_id = t_m['kb_id']
        log_printer.info('{}\t{}\t{}'.format(mention, kb_id, offset))
    
    log_printer.info('\n')
    
    for mention in doc.mention_list:
        log_printer.info(mention.word)
        for cand in mention.candidates:
            log_printer.info('{}\t{}\t{}'.format(cand.entity, cand.id, cand.score))

    log_printer.info('-----------------------------------\n')


def estimate_one(doc, text_json):
    """评估doc中识别的entity和text_json中指定的entity
    """
    target_mention = text_json['mention_data']
    right_count = 0
    wrong_count = 0
    for t_m in target_mention:
        found = False
        for i_m in doc.mention_list:
            if i_m.word == t_m['mention'] and str(i_m.start_pos) == str(t_m['offset']) and \
                len(i_m.candidates) > 0 and str(i_m.candidates[0].id) == t_m['kb_id']:
                    right_count += 1
                    found = True
        if t_m['kb_id'] != 'NIL' and not found:
            wrong_count += 1
    return right_count, wrong_count


if __name__ == '__main__':
    AppConfig.init_instance(config_file)
    agdistis = Agdistis()
    #doc = Document('苏华董事长简介 - 四川现代教育集团', False)
    #ret = agdistis.run(doc)
    
    test_file = '/Users/caoxiaojie/pythonCode/EntityLinking/data/baidu/train.json'
    
    right_count = 0
    wrong_count = 0
    count = 0
    with open(test_file, mode='r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            text = obj['text']
            doc = Document(text, False)
            ret_doc = agdistis.run(doc)
            r,w = estimate_one(ret_doc, obj)
            print_info(ret_doc, obj)
            right_count += r
            wrong_count += w
            count += 1
            if count > 0 and count % 100 == 0:
                print("完成：{}行, right:{}, wrong:{}".format(count, right_count, wrong_count))

    print('正确结果数量：', right_count, '\n错误结果数量：', wrong_count)
