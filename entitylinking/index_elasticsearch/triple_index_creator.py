# encoding=utf-8
import sys
import os
import logging
import timeit
import multiprocessing
from multiprocessing import Pool, cpu_count

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, parallel_bulk

from ..utils.file_utils import get_files

log_console = logging.StreamHandler(sys.stderr)
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(log_console)

# bulk单次的doc数量
bulk_count = 500

# 多少记录汇报一次
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
                }
            },
            "analyzer": {
                "jieba_index_analyzer": {
                    "tokenizer": "jieba_index",
                    "filter": [
                        "lowercase",
                        "jieba_stop"
                    ]
                },
                "jieba_index_all_analyzer": {
                    "tokenizer": "jieba_index_all",
                    "filter": [
                        "lowercase",
                        "jieba_stop"
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
    es = Elasticsearch()
    if es.indices.exists(indexname):
        default_logger.info("索引{}已经存在了".format(indexname))
        if not overwrite:
            return
        else:
            # 如果是覆盖，那么就删除原来的
            es.indices.delete(index=indexname)
    ret = es.indices.create(index=indexname, body=index_config)
    default_logger.info("创建索引，返回结果：{}".format(ret))
    start = timeit.default_timer()
    #write_doc_multi_process(indexname, data)
    write_doc_parallel(indexname, data)
    end = timeit.default_timer()
    default_logger.info("完成索引的创建，共耗时：{}".format(end - start))
    es.indices.put_settings(index=indexname, body=index_config_after)


def get_es_client():
    """获取ES Client
    """
    return Elasticsearch()


def write_doc_parallel(indexname, data_dir):
    """并发创建索引
    """
    start = timeit.default_timer()
    es = get_es_client()
    actions_iter = get_actions_iterator(indexname, data_dir)
    ret = parallel_bulk(es, actions_iter, thread_count=process_count,
                        chunk_size=bulk_count, queue_size=process_count*2)
    count = 0
    for ok, info in ret:
        count += 1
        if count > 0 and count % report_count == 0:
            end = timeit.default_timer()
            default_logger.info("完成{}行，耗时{}".format(count, end - start))
        if not ok:
            default_logger.info("出现错误：", info)
    end = timeit.default_timer()
    default_logger.info("完成{}行，耗时{}".format(count, end - start))


def get_actions_iterator(indexname, data_dir):
    """获取actions的迭代器
    """
    count = 0
    files = get_files(data_dir)

    start = timeit.default_timer()
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
