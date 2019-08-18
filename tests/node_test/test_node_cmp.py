import pytest

from entitylinking.graph.node import Node


@pytest.mark.node_cmp
def test_node_cmp():
    node_list = []
    node1 = Node("abc", 1, 'hits')
    node1.authority_weight = 11

    node2 = Node("efg", 1, 'hits')
    node2.authority_weight = 22

    node3 = Node("hij", 1, 'hits')
    node3.authority_weight = 33

    node_list.append(node1)
    node_list.append(node3)
    node_list.append(node2)

    result = sorted(node_list, key=lambda node: node.cmp_value)
    for node in result:
        print(node.value)

    assert True