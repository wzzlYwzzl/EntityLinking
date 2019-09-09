import networkx as nx
import matplotlib.pyplot as plt
from cacheout import Cache

from ..config.app_config import AppConfig
from ..base.document import Document
from ..graph.node import Node
from ..candidate.candidate_utils import CandidateUtils
from ..candidate.candidate import Candidate
from ..graph.neighbor_builder import insert_neighbors
from ..graph.hits import hits_analyze
from ..graph.pagerank import pagerank_analyze
from ..index_elasticsearch.triple_index_with_id import TripleIndex
import entitylinking.jieba as jieba


class Agdistis:
    """复现的AGDISTIS开源实体链接项目的算法
    https://github.com/dice-group/AGDISTIS
    """

    def __init__(self):
        # 候选实体所在图谱的关系节点的深度
        self._max_depth = int(AppConfig.instance().max_depth)
        self._algorithm = AppConfig.instance().algorithm
        es_endpoint = AppConfig.instance().es_endpoints
        indexname = AppConfig.instance().indexname
        TripleIndex.init_instance(es_endpoint, indexname)
        self._triple_index = TripleIndex.instance()
        #jieba.load_userdict(AppConfig.instance().user_dic)

        # 缓存
        self._cache = Cache(maxsize=10*1024, ttl=10*60)

    def run(self, doc):
        """算法的入口函数

        Arguments:
            doc -- {Document} 算法需要的进行链接的文本

        Returns:
            list<Mention> -- doc中包含的mention，mention中存储有实体链接的结果信息
        """
        cache_doc = self._cache.get(doc.text)
        if cache_doc:
            return cache_doc

        # 按照mention的长度从大到小排序
        doc.mention_list = sorted(doc.mention_list,
                                  key=lambda iterm: iterm.length, reverse=True)
        CandidateUtils.instance().add_candidates(doc)

        if len(doc.mention_list) <= 1 or self._algorithm == 'none':
            # 如果只有一个mention，不需要后面的算法
            self._cache.add(doc.text, doc)
            doc.sort_candidates()
            return doc

        # 创建有向图
        graph = nx.DiGraph()
        
        # 根据mentions添加候选实体到graph中
        self.add_candidates2graph(graph, doc)

        # 将候选实体在图谱中的相邻关系节点也插入到graph中
        insert_neighbors(graph, self._triple_index,
                         self._max_depth, self._algorithm)

        #options = {'node_color': 'black', 'node_size': 20, 'width': 1}
        #nx.draw_random(graph, **options)
        # plt.savefig('test.png')
        # plt.show()

        # 使用链接算法更新节点权重
        if self._algorithm == 'hits':
            hits_analyze(graph, iter=2)
        elif self._algorithm == 'pagerank':
            pagerank_analyze(graph, max_iter=50, threshhold=0.1)

        self.node2candidates(graph, doc)

        self._cache.add(doc.text, doc)
        return doc

    def add_candidates2graph(self, graph, doc):
        """将mentions的所有候选项都作为Node添加到graph中。
        """
        algorithm = AppConfig.instance().algorithm

        node_map = {}
        for mention in doc.mention_list:
            candidates = mention.candidates
            for candidate in candidates:
                if candidate.id in node_map:
                    node = node_map[candidate.id]
                    # 这里ids存放的是mention本身
                    node.ids.add(mention)
                else:
                    node = Node(candidate.id, candidate.entity,
                                0, algorithm, base_score=candidate.score)
                    node.ids.add(mention)
                    node_map[candidate.entity] = node

        for node in node_map.values():
            graph.add_node(node)

    def node2candidates(self, graph, doc):
        """将graph中的candidates添加到对应的mention中。
        """
        nodes = graph.nodes
        for node in nodes:
            for mention in node.ids:
                mention.candidates = []  # 先清空原来的候选项

        # 将node根据得分从大到小排序
        nodes = sorted(nodes, key=lambda node: node.cmp_value, reverse=True)
        for node in nodes:
            if len(node.ids) > 0:
                candidate = self.node2candidate(node)
                for mention in node.ids:
                    mention.candidates.append(candidate)

    def node2candidate(self, node):
        """将graph的node转换为candidate

        Arguments:
            node {Node} -- 表示图的节点

        Returns:
            Candidate -- 候选项
        """
        if len(node.ids) > 1:
            score = node.base_score
        else:
            score = node.score + node.base_score
        candidate = Candidate(entity=node.value, id=node.id, score=score)
        return candidate
