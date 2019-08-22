def pagerank_analyze(graph, max_iter, threshhold):
    """利用pagerank算法对graph的节点进行链接分析。

    Arguments:
        graph {DiGraph} -- networkx中的有向图
        max_iter {int} -- 最大迭代次数
        threshhold {int} -- 两次迭代整个graph的pagerank值更新量，
            低于这个值就暂停迭代 
    """
    node_count = graph.number_of_nodes()
    if node_count <= 0:
        return

    # 初始化与pagerank有关的值
    alpha = 0.85
    pagerank = 1.0 / node_count

    for node in graph.nodes:
        node.page_rank = pagerank
        node.page_rank_new = 0.0

    iter_num = 0
    distance = 0  # 表示两个迭代pagerank值的更新

    while iter_num < max_iter:
        random_walker = 0.0

        for node in graph.nodes:
            successors = graph.successors(node)
            successors_list = list(successors)
            if len(successors_list) > 0:
                pr = node.page_rank / len(successors_list)
                for suc_node in successors_list:
                    suc_node.page_rank_new += pr
            else:
                random_walker += node.page_rank / node_count

        for node in graph.nodes:
            pr_new = node.page_rank_new
            node.page_rank_new = (alpha * (pr_new + random_walker)) \
                + ((1-alpha)/node_count)

        # 计算distance，因为后面会normalization相应的pagerank值
        distance = compute_distance(graph)

        sum_page_rank = 0
        for node in graph.nodes:
            node.page_rank = node.page_rank_new
            node.page_rank_new = 0
            sum_page_rank += node.page_rank

        for node in graph.nodes:  # 归一化操作
            node.page_rank = node.page_rank / sum_page_rank

        iter_num += 1
        
        # 如果迭代前后的pagerank值变化小于阈值，就break
        if distance <= threshhold:
            break


def compute_distance(graph):
    """计算graph中，每个节点新旧pagerank的更新量
    """
    distance = 0.0
    for node in graph.nodes:
        distance += abs(node.page_rank - node.page_rank_new)
    return distance
