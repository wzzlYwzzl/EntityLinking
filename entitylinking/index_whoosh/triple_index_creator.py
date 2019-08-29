import os
import re
import datetime
import timeit
import logging

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage

from entitylinking.jieba.analyse import ChineseAnalyzer

from ..utils.file_utils import get_files

log_console = logging.StreamHandler(sys.stderr)
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(log_console)

# 打印日志的间隔，默认是一百万
report_period = 10000
# 基于jieba的analyzer
analyzer = ChineseAnalyzer()
analyzer_subject = ChineseAnalyzer(cut_all=False)
re_mention = '（.+）'


def triple_index_create(data, index_dir):
    """构建三元组索引，如果索引已经存在了，那么data中的内容会追加到index_dir
    目录下面的索引中

    Arguments:
        data {str} -- 要构建索引的cn-dbpedia数据目录或者单个文件
        index_dir {str} -- 索引存放的目录
    """
    storage = FileStorage(index_dir)
    storage.create()
    _create_triple_index(storage, data)


def _create_triple_index(storage, data):
    """将data数据创建成用jieba分词器的索引，用于
    不精准匹配搜索使用
    """
    schema = _create_jieba_schema()
    if storage.index_exists(indexname='triple'):
        ix = storage.open_index(indexname='triple')
    else:
        ix = storage.create_index(schema, indexname='triple')
    writer = ix.writer()
    _write_document(writer, data)
    writer.commit()


def _create_jieba_schema():
    """创建Schema，这里使用的是jieba分词器
    """
    schema = Schema(subject=TEXT(stored=True, analyzer=analyzer_subject),
                    subject_cutall=TEXT(stored=False, analyzer=analyzer),
                    predicate=TEXT(stored=True, analyzer=analyzer),
                    object=TEXT(stored=True, analyzer=analyzer))
    return schema


def _write_document(writer, data_dir):
    """将data_dir目录下的文件写入到writer中。
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
                    writer.add_document(
                        subject=fields[0].strip(),
                        subject_cutall=fields[0].strip(),
                        predicate=fields[1].strip(),
                        object=fields[2].strip()
                    )
                if count > 0 and count % report_period == 0:
                    end = timeit.default_timer()
                    default_logger.info("完成{}行，耗时{}".format(count, end-start))
    end = timeit.default_timer()
    default_logger.info("完成{}行，耗时{}秒".format(count, end-start))
    default_logger.info("完成索引创建")
