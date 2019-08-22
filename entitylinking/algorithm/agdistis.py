import networkx as nx
import matplotlib.pyplot as plt

from ..config.app_config import AppConfig
from ..base.document import Document
from ..graph.node import Node
from ..candidate.candidate_utils import CandidateUtils
from ..candidate.candidate import Candidate
from ..graph.neighbor_builder import insert_neighbors
from ..graph.hits import hits_analyze
from ..graph.pagerank import pagerank_analyze
from ..index_whoosh.triple_index import TripleIndex


class Agdistis:
    """复现的AGDISTIS开源实体链接项目的算法
    https://github.com/dice-group/AGDISTIS
    """

    def __init__(self):
        # 候选实体所在图谱的关系节点的深度
        self._max_depth = int(AppConfig.instance().max_depth)
        self._algorithm = AppConfig.instance().algorithm
        self._triple_index = TripleIndex(AppConfig.instance().index_dir)

    def run(self, doc):
        """算法的入口函数

        Arguments:
            doc -- {Document} 算法需要的进行链接的文本

        Returns:
            list<Mention> -- doc中包含的mention，mention中存储有实体链接的结果信息
        """
        # 创建有向图
        graph = nx.DiGraph()

        # 按照mention的长度从大到小排序
        mentions = sorted(doc.mention_list,
                          key=lambda iterm: iterm.length, reverse=True)
        # 根据mentions添加候选实体到graph中
        self.add_candidates2graph(graph, mentions)
        # 将候选实体在图谱中的相邻关系节点也插入到graph中
        insert_neighbors(graph, self._triple_index, self._max_depth, self._algorithm)

        options = { 'node_color': 'black', 'node_size': 20, 'width': 3}
        nx.draw_random(graph, **options)
        plt.savefig('test.png')
        #plt.show()

        # 使用链接算法更新节点权重
        if self._algorithm == 'hits':
            hits_analyze(graph, iter=20)
        elif self._algorithm == 'pagerank':
            pagerank_analyze(graph, max_iter=50, threshhold=0.1)

        self.add_candidates2mentions(graph, mentions)

        return mentions

    def add_candidates2graph(self, graph, mentions):
        """将mentions的所有候选项都作为Node添加到graph中。
        """
        algorithm = AppConfig.instance().algorithm

        node_map = {}
        for mention in mentions:
            candidates = CandidateUtils.instance().get_condidates(mention)
            for candidate in candidates:
                if candidate.entity in node_map:
                    node = node_map(candidate.entity)
                    # 这里ids存放的是mention本身
                    node.ids.add(mention)
                else:
                    node = Node(
                        candidate.entity, 0, algorithm)
                    node.ids.add(mention)
                    node_map[candidate.entity] = node

        for node in node_map.values():
            graph.add_node(node)

    def add_candidates2mentions(self, graph, mentions):
        """将graph中的candidates添加到对应的mention中。
        """
        nodes = graph.nodes
        # 将node根据得分从大到小排序
        nodes = sorted(nodes, key=lambda node: node.cmp_value, reverse=True)
        for node in nodes:
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
        candidate = Candidate(node.value, node.score)
        return candidate
