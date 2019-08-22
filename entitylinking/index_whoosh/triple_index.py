import whoosh.index as index
import whoosh.qparser as qparser
from whoosh.qparser import QueryParser


from ..config.app_config import AppConfig
from ..base.triple import Triple


class TripleIndex:
    """基于whoosh实现的triple索引
    """

    def __init__(self, index_dir):
        # 索引
        self._ix = index.open_dir(index_dir, indexname='triple')
        self._searcher = self._ix.searcher()
        # 用于返回具有相似度的结果
        self._query_parser_or = QueryParser(
            'subject', self._ix.schema, group=qparser.OrGroup)
        # 用于获取精准匹配的结果
        self._query_parser_and = QueryParser('subject', self._ix.schema)

    def search(self, subject=None, predicate=None, object=None, and_or='or', max_result_count=50):
        """对三元组索引执行查询。

        Returns
            list<triple> -- 三元组Triple的list
        """
        query_str = ""

        if subject != None:
            query_str += "subject:({}),".format(subject)

        if predicate != None:
            query_str += "predicate:({}),".format(predicate)

        if object != None:
            query_str += "object:({})".format(object)

        if and_or == 'or':
            q = self._query_parser_or.parse(query_str)
        else:
            q = self._query_parser_and.parse(query_str)

        results = self._searcher.search(q, limit=max_result_count)

        triples = []
        for result in results:
            subject = result['subject']
            predicate = result['predicate']
            object = result['object']
            triple = Triple(subject, predicate, object)
            triples.append(triple)

        return triples
