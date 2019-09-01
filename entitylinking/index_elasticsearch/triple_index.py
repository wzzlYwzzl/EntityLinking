import threading

from elasticsearch import Elasticsearch
from cacheout import LRUCache


from ..config.app_config import AppConfig
from ..base.triple import Triple
from ..candidate.candidate import Candidate


class TripleIndex:
    """基于whoosh实现的triple索引
    """
    _lock = threading.Lock()

    @classmethod
    def init_instance(cls, es_client=None):
        """初始化实例
        """
        with cls._lock:
            cls._instance = TripleIndex(es_client)

    @classmethod
    def instance(cls):
        """获取单实例
        """
        if not hasattr(cls, '_instance'):
            raise Exception("必须先调用TripleIndex的init_instance方法初始化实例")
        else:
            return cls._instance

    def __init__(self, es_client=None):
        # 索引
        if es_client:
            self.es = Elasticsearch([es_client])
        else:
            self.es = Elasticsearch()
        self.indexname = 'triple'

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
            q = self.build_search_query(subject, predicate, object, mode)
            results = self.search_triples(q, max_result_count)
            self._triple_cache.add(key, results)

        return results

    def build_search_query(self, subject=None, predicate=None, object=None, mode='or'):
        """构建关于三元组的查询语句
        """
        query_list = []

        if subject:
            query_list.append("subject:({})".format(subject))

        if predicate:
            query_list.append("predicate:({})".format(predicate))

        if object:
            query_list.append("object:({})".format(object))

        if mode == 'or':
            query_str = " OR ".join(query_list)
        else:
            query_str = " AND ".join(query_list)

        query = {
            "query":{
                "query_string": {
                    "query": query_str
                }
            }
        }
        return query

    def build_filter_query(self, subject=None, object=None):
        """构建关于三元组的查询语句
        """
        query_str = ""

        if subject:
            query_str += "subject:({})".format(subject)

        if object:
            query_str += " AND (object:({}) OR subject:({}))".format(object, object)

        query = {
            "query":{
                "query_string": {
                    "query": query_str
                }
            }
        }
        return query

    def search_triples(self, q, max_result_count):
        """搜索结果使用三元组来表示
        """
        results = self.es.search(index=self.indexname, body=q, size=max_result_count)

        hits_list = results['hits']['hits']
        triples = []
        for result in hits_list:
            source = result['_source']
            subject = source['subject']
            predicate = source['predicate']
            object = source['object']
            triple = Triple(subject, predicate, object)
            triples.append(triple)

        return triples

    def search_candidates(self, subject=None, object=None, max_result_count=20):
        """搜索结果用candidate来表示，这里包含搜索的得分
        """
        key = self._get_cache_key(
            subject, None, object, max_result_count)

        results = self._candidate_cache.get(key)
        if not results:
            q = self.build_filter_query(subject, object)
            se_results = self.es.search(index=self.indexname, body=q, size=max_result_count)
            hits_list = se_results['hits']['hits']
            results = []
            for result in hits_list:
                subject = result['_source']['subject']
                score = result['_score']
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
