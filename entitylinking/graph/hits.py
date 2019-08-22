def hits_analyze(graph, iter):
    """对graph进行hits分析，更新graph中每个节点的hub值和authority值。

    Arguments:
        graph {DiGraph} -- networkx的有向图
        iter {int} -- 迭代次数
    """
    for _ in range(iter):
        for node in graph.nodes:
            tmp = 0.0
            predecessors = graph.predecessors(node)
            for node_tmp in predecessors:
                tmp += node_tmp.hub_weight
            node.unnormarized_authority_weight = tmp * node.authority_weight_for_calculation

            tmp = 0.0
            successors = graph.successors(node)
            for node_tmp in successors:
                tmp += node_tmp.authority_weight
            node.unnormarized_hub_weight = tmp * node.hub_weight_for_calculation

        # normalize the weight
        sum_authority = 0.0
        sum_hub = 0.0
        for node in graph.nodes:
            sum_authority += node.authority_weight
            sum_hub += node.hub_weight

        for node in graph.nodes:
            node.authority_weight = node.unnormarized_authority_weight / sum_authority
            node.hub_weight = node.unnormarized_hub_weight / sum_hub
