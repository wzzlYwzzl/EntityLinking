class Node:
    """图的一个节点
    """

    def __init__(self, value, level, algorithm, base_score=0):
        # 与这个Node有关的内容不止一个，将它们的唯一标识都添加到ids
        self.ids = set()

        # 当前Node节点存储的取值信息
        self.value = value
        # 用于存储节点在图中的相对某个节点的深度
        self.level = level

        # 算法名称，hits 或者 pagerank
        self.algorithm = algorithm
        self.page_rank = 0
        self.page_rank_new = 0

        # 下面用于hits算法
        self.hub_weight = 1
        self.authority_weight = 1
        self.hub_weight_for_calculation = 1
        self.authority_weight_for_calculation = 1
        # 用于计算hub_weight时，临时存储中间值
        self.unnormarized_hub_weight = 1
        self.unnormarized_authority_weight = 1

        # 当前node的有其他逻辑确定的初始得分
        self.base_score = base_score

    @property
    def score(self):
        """获取当前节点的score
        """
        if self.algorithm == 'hits':
            return self.authority_weight + self.base_score
        elif self.algorithm == 'pagerank':
            return self.page_rank + self.base_score
        else:
            return 0

    @property
    def cmp_value(self):
        """获取排序时使用的值
        """
        if self.algorithm == 'hits':
            return self.authority_weight + self.base_score
        elif self.algorithm == 'pagerank':
            return self.page_rank + self.base_score
        else:
            return 0

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, node):
        """重载==，判断依据Node的value是否相等
        """
        if isinstance(node, Node):
            if self.value == node.value:
                return True
            else:
                return False
        else:
            return False
