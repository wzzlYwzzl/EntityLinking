from .candidate_filter import CandidateFilter
from ..index_whoosh.triple_index import TripleIndex


class SearchScoreFilter(CandidateFilter):
    """通过利用文本对三元组进行搜索，过滤掉候选实体中在搜索结果里得分不高的
    """

    def filter(self, doc, mention, candidates):
        """过滤候选实体
        """
        mention_context = ' '.join(mention.context).strip()
        if mention_context:
            triples = TripleIndex.instance().search(subject=mention.word,
                                                    object=mention_context,
                                                    mode='filter',
                                                    max_result_count=20)
            candidate_dic = {}
            for cand in candidates:
                candidate_dic[cand.entity] = cand

            ret_set = set()
            for triple in triples:
                if triple.subject in candidate_dic:
                    ret_set.add(candidate_dic[triple.subject])

            if len(ret_set) == 0:
                return candidates
            else:
                return list(ret_set)
