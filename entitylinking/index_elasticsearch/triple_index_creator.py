import sys
import logging
import timeit
import multiprocessing
from multiprocessing import Process
import threading
import queue

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from ..utils.file_utils import get_files

log_console = logging.StreamHandler(sys.stderr)
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(log_console)

# bulk单次的doc数量
bulk_count = 30000
# 并发数量
process_count = 2


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
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "subject": {
                "type": "text",
                "analyzer": "jieba_index_analyzer",
                "store": True
            },
            "predicate": {
                "type": "keyword"
            },
            "object": {
                "type": "text",
                "store": True
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
    _write_doc_multi_process(es, indexname, data)
    es.indices.put_settings(index=indexname, body=index_config_after)


def one_process(es, indexname, actions, count, start):
    """单个进程的处理逻辑
    """
    success, _ = bulk(es, actions, index=indexname, raise_on_error=True)
    end = timeit.default_timer()
    default_logger.info("状态: {}, 完成{}行, 耗时：{}".format(success, count, end - start))


def _write_doc_multi_process(es, indexname, data_dir):
    """多线程模式写入数据
    """
    pool = multiprocessing.Pool(processes=process_count)

    actions_iter = _get_actions_iterator(indexname, data_dir)
    count = 0
    start = timeit.default_timer()
    for actions in actions_iter:
        count += len(actions)
        pool.apply_async(one_process, args=(es, indexname, actions, count, start))
    pool.close()
    pool.join()


def _write_document(es, indexname, data_dir):
    """将data_dir目录下的文件写入到writer中。
    """
    actions_iter = _get_actions_iterator(indexname, data_dir)
    for actions in actions_iter:
        pass
    count = 0
    files = get_files(data_dir)

    start = timeit.default_timer()
    actions = []
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
                    actions.append(action)
                if count > 0 and count % bulk_count == 0:
                    success, _ = bulk(
                        es, actions, index=indexname, raise_on_error=True)
                    end = timeit.default_timer()
                    default_logger.info("状态: {}, 完成{}行，耗时{}".format(
                        success, count, end-start))
    if len(actions) > 0:
        bulk(es, actions, index=indexname, raise_on_error=True)
    end = timeit.default_timer()
    default_logger.info("完成{}行，耗时{}秒".format(count, end-start))
    default_logger.info("完成索引创建")


def _get_actions_iterator(indexname, data_dir):
    """获取actions的迭代器，每次返回的是指定数量的actions
    """
    count = 0
    files = get_files(data_dir)

    start = timeit.default_timer()
    actions = []
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
                    actions.append(action)
                if count > 0 and count % bulk_count == 0:
                    yield actions
    if len(actions) > 0:
        yield actions


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
