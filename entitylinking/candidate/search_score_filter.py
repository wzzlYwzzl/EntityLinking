from .candidate_filter import CandidateFilter
from ..index_elasticsearch.triple_index import TripleIndex


class SearchScoreFilter(CandidateFilter):
    """通过利用文本对三元组进行搜索，过滤掉候选实体中在搜索结果里得分不高的
    """

    def filter(self, doc, mention, candidates):
        """过滤候选实体
        """
        mention_context = mention.context_str(' ')
        if mention_context:
            candidates_search = TripleIndex.instance().search_candidates(subject=mention.word,
                                                                         object=mention_context,
                                                                         max_result_count=40)
            candidate_dic = {}
            for cand in candidates:
                candidate_dic[cand.entity] = cand

            ret_set = set()
            for cand in candidates_search:
                if cand.entity in candidate_dic:
                    ret_set.add(cand)

            if len(ret_set) == 0:
                return candidates
            else:
                self.score_normalization(ret_set)
                return list(ret_set)
        else:
            return candidates

    def score_normalization(self, candidates):
        """得分归一化
        """
        sum_score = 0
        for cand in candidates:
            sum_score += cand.score

        for cand in candidates:
            cand.score = cand.score / sum_score
