import networkx as nx

from ..config.app_config import AppConfig
from ..base.document import Document
from ..graph.node import Node
from ..candidate.candidate_utils import CandidateUtils


class Agdistis:
    """复现的AGDISTIS开源实体链接项目的算法
    https://github.com/dice-group/AGDISTIS
    """

    def __init__(self):
        # 候选实体所在图谱的关系节点的深度
        self._max_depth = AppConfig.instance().max_depth
        self._algorithm = AppConfig.instance().algorithm

    def run(self, doc):
        """算法的入口函数

        Arguments:
            doc -- {Document} 算法需要的进行链接的文本
        """
        # 创建有向图
        graph = nx.DiGraph()

        # 按照mention的长度从大到小排序
        mentions = sorted(doc.mention_list,
                          key=lambda iterm: iterm.length, reverse=True)

        for mention in mentions:
            candidates = None
