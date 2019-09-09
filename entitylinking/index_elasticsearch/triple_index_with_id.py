import threading
import timeit
import re

from elasticsearch import Elasticsearch
from cacheout import LRUCache


from ..config.app_config import AppConfig
from ..base.triple import Triple
from ..candidate.candidate import Candidate
from ..log.log_manager import LogManager


class TripleIndex:
    """基于whoosh实现的triple索引
    """
    _lock = threading.Lock()

    @classmethod
    def init_instance(cls, es_client=None, indexname='triple'):
        """初始化实例
        """
        with cls._lock:
            cls._instance = TripleIndex(es_client, indexname)

    @classmethod
    def instance(cls):
        """获取单实例
        """
        if not hasattr(cls, '_instance'):
            raise Exception("必须先调用TripleIndex的init_instance方法初始化实例")
        else:
            return cls._instance

    def __init__(self, es_client=None, indexname='triple_id'):
        # 索引
        if es_client:
            end_points = es_client.strip().split('$')
            self.es = Elasticsearch(
                end_points, timeout=60, max_retries=10, retry_on_timeout=True)
        else:
            self.es = Elasticsearch()
        self.indexname = indexname

        # 搜索缓存
        self._triple_cache = LRUCache(maxsize=10 * 1024 * 1024, ttl=10 * 60)
        self._candidate_cache = LRUCache(maxsize=10 * 1024 * 1024, ttl=10 * 60)

    def search(self, subject_id=None, subject=None, predicate=None,
               object=None, mode='or', max_result_count=10):
        """对三元组索引执行查询。

        Arguments:
            mode {str} -- 搜索模式，目前有：and、or、filter

        Returns
            list<Triple> -- 三元组Triple的list
        """
        key = self._get_cache_key(
            subject_id, subject, predicate, object, mode, max_result_count)
        results = self._triple_cache.get(key)
        if not results:
            q = self.build_search_query(
                subject_id, subject, predicate, object, mode)
            start = timeit.default_timer()
            results = self.search_triples(q, mode, max_result_count)
            end = timeit.default_timer()
            LogManager.instance().debug("查询：{},耗时：{}".format(q, end - start))
            self._triple_cache.add(key, results)

        return results

    def build_search_query(self, subject_id=None, subject=None, predicate=None, object=None, mode='or'):
        """构建关于三元组的查询语句
        """
        query_list = []

        if subject_id:
            query_list.append("subject_id:({})".format(subject_id))

        if subject:
            query_list.append("subject:({})".format(subject))

        if predicate:
            query_list.append("predicate:({})".format(predicate))

        if object:
            query_list.append("object:({})".format(object))

        operator = "OR"

        if mode == 'or':
            query_str = " OR ".join(query_list)
        else:
            query_str = " AND ".join(query_list)
            operator = "AND"

        query = {
            "query": {
                "query_string": {
                    "query": query_str,
                    "default_operator": operator
                }
            }
        }
        return query

    def build_filter_query(self, subject_ids=None, subject=None, object=None):
        """构建关于三元组的查询语句

        Arguments:
            subject_ids {list} -- id列表
        """
        query_str = ""

        if subject:
            query_str += "subject:({})".format(subject)

        if object:
            query_str += " AND search_field:({})".format(object, object)

        if subject_ids:
            tmp = ' OR '.join(['subject_id:'+ str(item) for item in subject_ids])
            query_str += " AND ({})".format(tmp)

        query = {
            "query": {
                "query_string": {
                    "query": query_str
                }
            }
        }

        print("fiter:", query)
        return query

    def search_triples(self, q, mode, max_result_count):
        """搜索结果使用三元组来表示
        """
        df = 'OR' if mode == 'or' else 'AND'

        results = self.es.search(
            index=self.indexname, body=q, size=max_result_count)

        hits_list = results['hits']['hits']
        triples = []
        for result in hits_list:
            source = result['_source']
            subject_id = source['subject_id']
            subject = source['subject']
            predicate = source['predicate']
            subject_id = source['subject_id']
            object = re.sub(r'<a>|</a>', '', source['object'])
            object_id = source['object_id']
            triple = Triple(subject_id, subject, predicate, object, object_id)
            triples.append(triple)

        return triples

    def search_candidates(self, subject_ids=None, subject=None, object=None, max_result_count=20):
        """搜索结果用candidate来表示，这里包含搜索的得分
        """
        key = self._get_cache_key(
            subject_ids, subject, None, object, max_result_count)

        results = self._candidate_cache.get(key)
        if not results:
            q = self.build_filter_query(subject_ids, subject, object)
            start = timeit.default_timer()
            se_results = self.es.search(
                index=self.indexname, body=q, size=max_result_count)
            end = timeit.default_timer()
            LogManager.instance().debug("查询：{},耗时：{}".format(q, end - start))
            hits_list = se_results['hits']['hits']
            results = []
            for result in hits_list:
                subject = result['_source']['subject']
                subject_id = result['_source']['subject_id']
                score = result['_score']
                candidate = Candidate(subject, subject_id, score)
                results.append(candidate)
            self._candidate_cache.add(key, results)

        return results

    def _get_cache_key(self, subject_ids=None, subject=None,
                       predicate=None, object=None, mode='or', max_result_count=20):
        """获取缓存数据时使用的key
        """
        key = ""
        if subject_ids:
            key += 'id:{}'.format(str(subject_ids))

        if subject:
            key += 'sub:{}'.format(subject)

        if object:
            key += 'obj:{}'.format(object)

        if predicate:
            key += 'pre:{}'.format(predicate)

        key += 'mode:{},count:{}'.format(mode, max_result_count)

        return key
