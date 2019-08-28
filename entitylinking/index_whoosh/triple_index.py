import threading

import whoosh.index as index
import whoosh.qparser as qparser
from whoosh.qparser import QueryParser
from cacheout import LRUCache


from ..config.app_config import AppConfig
from ..base.triple import Triple
from ..candidate.candidate import Candidate


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

        # 搜索缓存
        self._triple_cache = LRUCache(maxsize=10 * 1024 * 1024, ttl=10 * 60)
        self._candidate_cache = LRUCache(maxsize=10 * 1024 * 1024, ttl=10 * 60)

    def search(self, subject=None, predicate=None, object=None, mode='or', max_result_count=20):
        """对三元组索引执行查询。

        Arguments:
            mode {str} -- 搜索模式，目前有：and、or、filter

        Returns
            list<Triple> -- 三元组Triple的list
        """
        key = self._get_cache_key(
            subject, predicate, object, mode, max_result_count)
        results = self._triple_cache.get(key)
        if not results:
            q = self.build_query(subject, predicate, object, mode)
            results = self.search_triples(q, max_result_count)
            self._triple_cache.add(key, results)

        return results

    def build_query(self, subject=None, predicate=None, object=None, mode='or'):
        """构建关于三元组的查询语句
        """
        query_list = []

        if subject:
            query_list.append("subject:({})".format(subject))

        if predicate:
            query_list.append("predicate:({})".format(predicate))

        if object:
            query_list.append("object:({})".format(object))

        if mode == 'filter':
            query_str = " AND ".join(query_list)
            if object:
                query_str += " OR subject:({})".format(object)
        else:
            query_str = ",".join(query_list)

        if mode == 'or' or mode == 'filter':
            q = self._query_parser_or.parse(query_str)
        else:
            q = self._query_parser_and.parse(query_str)

        return q

    def search_triples(self, q, max_result_count):
        """搜索结果使用三元组来表示
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

    def search_candidates(self, subject=None, predicate=None, object=None, mode='or', max_result_count=20):
        """搜索结果用candidate来表示，这里包含搜索的得分
        """
        key = self._get_cache_key(
            subject, predicate, object, mode, max_result_count)
        
        results = self._candidate_cache.get(key)
        if not results:
            q = self.build_query(subject, predicate, object, mode)
            se_results = self._searcher.search(q, limit=max_result_count)

            results = []
            for result in se_results:
                subject = result['subject']
                score = result.score
                candidate = Candidate(subject, score)
                results.append(candidate)
            self._candidate_cache.add(key, results)

        return results

    def _get_cache_key(self, subject=None, predicate=None, object=None, mode='or', max_result_count=20):
        """获取缓存数据时使用的key
        """
        key = ""
        if subject:
            key += 'sub:{}'.format(subject)

        if object:
            key += 'obj:{}'.format(object)

        if predicate:
            key += 'pre:{}'.format(predicate)

        key += 'mode:{},count:{}'.format(mode, max_result_count)

        return key
