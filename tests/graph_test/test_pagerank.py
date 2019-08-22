import pytest
import networkx as nx

from entitylinking.graph.node import Node
from entitylinking.graph.pagerank import pagerank_analyze


@pytest.mark.pagerank
def test_pagerank():
    DG = nx.DiGraph()
    node1 = Node("abc", 1, 'hits')
    DG.add_node(node1)

    node2 = Node("efg", 1, 'hits')
    DG.add_node(node2)

    node3 = Node("hij", 1, 'hits')
    DG.add_node(node3)

    DG.add_edges_from([(node1, node2), (node2, node3)])

    pagerank_analyze(DG, 10, 0.1)

    assert True
