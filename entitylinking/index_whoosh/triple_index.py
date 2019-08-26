import threading

import entitylinking.whoosh.index as index
import entitylinking.whoosh.qparser as qparser
from entitylinking.whoosh.qparser import QueryParser


from ..config.app_config import AppConfig
from ..base.triple import Triple


class TripleIndex:
    """基于whoosh实现的triple索引
    """
    _lock = threading.Lock()

    @classmethod
    def init_instance(cls, index_dir):
        """初始化实例
        """
        with cls._lock:
            cls._instance = TripleIndex(index_dir)

    @classmethod
    def instance(cls):
        """获取单实例
        """
        if not hasattr(cls, '_instance'):
            raise Exception("必须先调用TripleIndex的init_instance方法初始化实例")
        else:
            return cls._instance

    def __init__(self, index_dir):
        # 索引
        self._ix = index.open_dir(index_dir, indexname='triple')
        self._searcher = self._ix.searcher()
        # 用于返回具有相似度的结果
        self._query_parser_or = QueryParser(
            'subject', self._ix.schema, group=qparser.OrGroup)
        # 用于获取精准匹配的结果
        self._query_parser_and = QueryParser('subject', self._ix.schema)

    def search(self, subject=None, predicate=None, object=None, mode='or', max_result_count=50):
        """对三元组索引执行查询。

        Arguments:
            mode {str} -- 搜索模式，目前有：and、or、filter

        Returns
            list<Triple> -- 三元组Triple的list
        """
        q = self.build_query(subject, predicate, object, mode)
        return self.search_triples(q, max_result_count)

    def build_query(self, subject=None, predicate=None, object=None, mode='or'):
        """构建关于三元组的查询语句
        """
        query_list = []

        if subject != None:
            query_list.append("subject:({}),".format(subject))

        if predicate != None:
            query_list.append("predicate:({}),".format(predicate))

        if object != None:
            query_list.append("object:({})".format(object))

        if mode == 'filter':
            query_str = " AND ".join(query_list)
        else:
            query_str = ",".join(query_list)

        if mode == 'or' or mode == 'filter':
            q = self._query_parser_or.parse(query_str)
        else:
            q = self._query_parser_and.parse(query_str)

        return q

    def search_triples(self, q, max_result_count):
        """
        """
        results = self._searcher.search(q, limit=max_result_count)

        triples = []
        for result in results:
            subject = result['subject']
            predicate = result['predicate']
            object = result['object']
            triple = Triple(subject, predicate, object)
            triples.append(triple)

        return triples
