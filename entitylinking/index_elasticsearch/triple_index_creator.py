# encoding=utf-8
import sys
import os
import logging
import timeit
import multiprocessing
from multiprocessing import Pool, cpu_count

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, streaming_bulk

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
                        "jieba_stop",
                        "jieba_synonym"
                    ]
                },
                "jieba_index_all_analyzer": {
                    "tokenizer": "jieba_index_all",
                    "filter": [
                        "lowercase",
                        "jieba_stop",
                        "jieba_synonym"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
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


def triple_index_create(indexname='triple', data=None, overwrite=False):
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
    write_doc_multi_process(indexname, data)
    end = timeit.default_timer()
    default_logger.info("完成索引的创建，共耗时：{}".format(end - start))
    es.indices.put_settings(index=indexname, body=index_config_after)


def get_es_client():
    """获取ES Client
    """
    return Elasticsearch(timeout=60, max_retries=10, retry_on_timeout=True)


def write_doc_multi_process(indexname, data_dir):
    """多进程模式写入数据，按照文件创建进程
    """
    pool = Pool(processes=process_count)
    files = get_files(data_dir)
    for file in files:
        pool.apply_async(write_document_one_file, args=(indexname, file))
    pool.close()
    pool.join()


def write_document_one_file(indexname, file_name):
    """将file_name文件写入到writer中。
    """
    count = 0
    start = timeit.default_timer()
    actions = []

    es = get_es_client()
    try:
        action_iter = get_actions_iterator(indexname, file_name)
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


def get_actions_iterator(indexname, data_dir):
    """获取actions的迭代器，每次返回的是指定数量的actions
    """
    count = 0
    files = get_files(data_dir)
    for file in files:
        with open(file, mode='r', encoding='utf8') as f:
            for line in f:
                fields = line.split('\t')
                if len(fields) == 3:
                    count += 1
                    action = _build_action(indexname=indexname,
                                           subject=fields[0].strip(),
                                           predicate=fields[1].strip(),
                                           object=fields[2].strip())
                    yield action


def _build_action(indexname, subject, predicate, object):
    """创建一个bulk使用的action
    """
    action = {
        '_index': indexname,
        '_op_type': 'index',  # 这个操作表示索引文档
        '_source': {
            'subject': subject,
            'predicate': predicate,
            'object': object
        }
    }

    return action
