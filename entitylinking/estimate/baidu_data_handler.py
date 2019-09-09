"""采用多进程的方式，将要构建索引的文件切分为多个，每个文件用独立的进程来处理
速度非常快。这里创建的索引是带有id的。
"""

# encoding=utf-8
import sys
import os
import json
import logging
import timeit
import multiprocessing
from multiprocessing import Pool, cpu_count

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from ..utils.file_utils import get_files

log_console = logging.StreamHandler(sys.stderr)
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(log_console)

# bulk单次的doc数量
bulk_count = 1000

report_count = 20000
# 并发数量
process_count = cpu_count()

# 创建索引时使用的配置，创建后要修改这个配置
index_config = {
    'settings': {
        "refresh_interval": "-1",
        "merge.policy.max_merged_segment": "1000mb",
        "translog.durability": "async",
        "translog.flush_threshold_size": "2gb",
        "translog.sync_interval": "100s",
        "analysis": {
            "filter": {
                "jieba_stop": {
                    "type": "stop",
                    "stopwords_path": "stopwords/stopwords.txt"
                },
                "jieba_synonym": {
                    "type": "synonym",
                    "synonyms_path": "synonyms/synonyms.txt",
                    "lenient": True
                }
            },
            "analyzer": {
                "jieba_index_analyzer": {
                    "tokenizer": "jieba_index",
                    "filter": [
                        "lowercase",
                        "jieba_stop"  # ,
                        # "jieba_synonym"
                    ]
                },
                "jieba_index_all_analyzer": {
                    "tokenizer": "jieba_index_all",
                    "filter": [
                        "lowercase",
                        "jieba_stop"  # ,
                        # "jieba_synonym"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "subject_id": {
                "type": "integer"
            },
            "subject": {
                "type": "text",
                "analyzer": "jieba_search",
                "store": True,
                "copy_to": "search_field"
            },
            "predicate": {
                "type": "keyword"
            },
            "object": {
                "type": "text",
                "store": True,
                "analyzer": "jieba_index_analyzer",
                "copy_to": "search_field"
            },
            "object_id": {
                "type": "integer"
            },
            "search_field": {
                "type": "text",
                "analyzer": "jieba_index_all_analyzer"
            }
        }
    }
}

index_config_after = {
    'settings': {
        "refresh_interval": "30s",
    }
}

# 存放subject:id对应关系
id_dict = {}


def triple_index_create(indexname='triple_baidu', json_dir=None, overwrite=False):
    """创建三元组的索引
    """
    # 初始化ES
    es = get_es_client()
    if es.indices.exists(indexname):
        default_logger.info("索引{}已经存在了".format(indexname))
        if overwrite:
            # 如果是覆盖，那么就删除原来的
            es.indices.delete(index=indexname)
            default_logger.info("删除索引:{}".format(indexname))
            ret = es.indices.create(index=indexname, body=index_config)
            default_logger.info("创建索引，返回结果：{}".format(ret))
    else:
        ret = es.indices.create(index=indexname, body=index_config)
        default_logger.info("创建索引，返回结果：{}".format(ret))
    start = timeit.default_timer()
    write_doc_multi_process(indexname, json_dir)
    end = timeit.default_timer()
    default_logger.info("完成索引的创建，共耗时：{}".format(end - start))
    es.indices.put_settings(index=indexname, body=index_config_after)


def get_es_client():
    """获取ES Client
    """
    return Elasticsearch(timeout=60, max_retries=10, retry_on_timeout=True)


def write_doc_multi_process(indexname, json_dir):
    """多进程模式写入数据，按照文件创建进程
    """
    pool = Pool(processes=process_count)
    files = get_files(json_dir)
    for file in files:
        pool.apply_async(write_document_one_file, args=(indexname, file))
    pool.close()
    pool.join()


def write_document_one_file(indexname, json_file):
    """将file_name文件写入到writer中。
    """
    count = 0
    start = timeit.default_timer()
    actions = []

    es = get_es_client()
    try:
        action_iter = get_actions_iterator(indexname, json_file)
        ret = streaming_bulk(es, action_iter, chunk_size=bulk_count)
        for ok, info in ret:
            count += 1
            if count > 0 and count % report_count == 0:
                end = timeit.default_timer()
                default_logger.info("进程:{}, 状态: {}, 完成{}行，耗时{}".format(
                    os.getpid(), ok, count, end-start))

        end = timeit.default_timer()
        default_logger.info("进程 {} 完成{}行，耗时{}秒".format(
            os.getpid(), count, end-start))
        default_logger.info("进程{}完成索引创建".format(os.getpid()))
    except Exception as e:
        default_logger.info("出现异常:{}".format(e))


def get_actions_iterator(indexname, json_file):
    """获取actions的迭代器，每次返回的是指定数量的actions
    """
    count = 0
    with open(json_file, mode='r', encoding='utf-8') as f_json:
        for line in f_json:
            obj = json.loads(line)
            subject_id = obj.subject_id
            subject = obj.subject
            spo_list = obj.data
            for spo in spo_list:
                action = _build_action(
                    indexname, subject_id, subject, spo.predicate, spo.object)
                yield action


def _build_action(indexname, subject_id, subject, predicate, object):
    """创建一个bulk使用的action
    """
    subject_id = id_dict[subject]

    if object in id_dict:
        object_id = id_dict[object]
    else:
        object_id = 0

    action = {
        '_index': indexname,
        '_op_type': 'index',  # 这个操作表示索引文档
        '_source': {
            'subject_id': subject_id,
            'subject': subject,
            'predicate': predicate,
            'object': object,
            'object_id': object_id
        }
    }

    return action


def handle_json_data(json_data, mention_file):
    """处理百度提供的json格式的数据，将其处理为SPO的形式
    """
    with open(json_data, mode='r', encoding='utf-8') as f_json:
        with open(mention_file, mode='w+', encoding='utf-8') as f_mention:
            for line in f_json:
                data = json.loads(line)

if __name__ == '__main__':
    json_dir = '/Users/caoxiaojie/pythonCode/EntityLinking/data/baidu/kb_data'
    triple_index_create(json_dir=json_dir, overwrite=True)