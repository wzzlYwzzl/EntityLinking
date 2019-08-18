class Node:
    """图的一个节点
    """

    def __init__(self, value, level, algorithm):
        # 同一个value可能有多个，这个时候需要在node里添加id作为唯一标识
        self.ids = set()

        # 当前Node节点存储的取值信息
        self.value = value
        self.level = level

        # 算法名称，hits 或者 pagerank
        self.algorithm = algorithm
        self.page_rank = 0
        self.page_rank_new = 0

        # 有向图的之前的节点和之后的节点
        self.successors = set()
        self.predecessors = set()

        # 下面用于hits算法
        self.hub_weight = 1
        self.authority_weight = 1
        self.hub_weight_for_calculation = 1
        self.authority_weight_for_calculation = 1
        self.unnormarized_hub_weight = 1
        self.unnormarized_authority_weight = 1

    @property
    def cmp_value(self):
        """获取排序时使用的值
        """
        if self.algorithm == 'hits':
            return self.authority_weight
        elif self.algorithm == 'pagerank':
            return self.page_rank
        else:
            return 0

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, node):
        """重载==，判断依据Node的value是否相等
        """
        if self.value == node.value:
            return True
        else:
            return False
