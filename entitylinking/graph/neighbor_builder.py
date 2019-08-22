import sys
from queue import Queue

from ..config.app_config import AppConfig
from ..graph.node import Node

sys.setrecursionlimit(100000)

def insert_neighbors(graph, triple_index, max_depth, algorithm):
    """将graph中的node，按照其在图谱中的SPO关系，扩充其上下文。
    扩充的链接深度最大不能超过max_depth
    """
    node_queue = Queue()

    nodes = graph.nodes()
    for node in nodes:
        node_queue.put(node)

    while not node_queue.empty():
        node = node_queue.get()
        level = node.level
        if level > max_depth:
            continue
        else:
            neighbor_triples = get_direct_neighbors(
                triple_index, node, max_depth)
            for triple in neighbor_triples:
                if triple.object:
                    new_level = level + 1
                    new_node = Node(triple.object, new_level, algorithm)
                    node_queue.put(new_node)
                    graph.add_edge(node, new_node, predicate=triple.predicate)


def get_direct_neighbors(triple_index, node, max_depth):
    """获取以node为SPO中的S的所有三元组，由于现在三元组存储在lucene中，所以
    获取neighbors三元组的方法就是index查询。
    """
    subject = node.value
    triples = triple_index.search(subject=subject, and_or='and')
    return triples
