import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, TermQuery, BooleanQuery, BooleanClause, FuzzyQuery
from org.apache.lucene.store import MMapDirectory

from .lucene_helper import SUBJECT_FIELD, OBJECT_FIELD, PREDICATE_FIELD

from ..config.app_config import AppConfig
from .lucene_helper import init_lucene
from ..base.triple import Triple


class TripleIndex:
    """用于对三元组数据进行索引查询
    """

    def __init__(self):
        # 初始化lucene
        init_lucene()
        self._searcher = self._create_index_searcher()
        self._default_result_count = int(
            AppConfig.instance().default_search_count)

    def _create_index_searcher(self):
        """构建一个用于执行检索的IndexSearcher
        """
        index_dir = AppConfig.instance().index_dir
        directory = MMapDirectory(Paths.get(index_dir))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        return searcher

    def search(self, subject=None, predicate=None, object=None, max_result_count=5):
        """对三元组索引执行查询
        """
        max_result_count = self._default_result_count
        bq = BooleanQuery.Builder()

        if subject != None:
            term_query = TermQuery(Term(SUBJECT_FIELD, subject))
            bq.add(term_query, BooleanClause.Occur.MUST)

        if predicate != None:
            term_query = TermQuery(Term(PREDICATE_FIELD, predicate))
            bq.add(term_query, BooleanClause.Occur.MUST)

        if object != None:
            term_query = TermQuery(Term(OBJECT_FIELD, object))
            bq.add(term_query, BooleanClause.Occur.MUST)

        query = bq.build()
        return self._get_triples(query, max_result_count)

    def _get_triples(self, query, max_result_count):
        """从索引中查询，获取三元组
        """

        triple_list = []

        score_docs = self._searcher.search(query, max_result_count).scoreDocs
        for scoreDoc in score_docs:
            doc = self._searcher.doc(scoreDoc.doc)
            s = doc.get(SUBJECT_FIELD)
            p = doc.get(PREDICATE_FIELD)
            o = doc.get(OBJECT_FIELD)
            triple = Triple(s, p, o)
            triple_list.append(triple)

        return triple_list

    def fuzzy_search(self, subject=None, predicate=None, object=None, max_result_count=5):
        """模糊查询
        """
        max_result_count = self._default_result_count
        bq = BooleanQuery.Builder()

        if subject != None:
            term_query = FuzzyQuery(Term(SUBJECT_FIELD, subject))
            bq.add(term_query, BooleanClause.Occur.MUST)

        if predicate != None:
            term_query = FuzzyQuery(Term(PREDICATE_FIELD, predicate))
            bq.add(term_query, BooleanClause.Occur.MUST)

        if object != None:
            term_query = FuzzyQuery(Term(OBJECT_FIELD, object))
            bq.add(term_query, BooleanClause.Occur.MUST)

        query = bq.build()
        return self._get_triples(query, max_result_count)
