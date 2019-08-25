class Candidate:
    """标识mention的一个候选实体
    """

    def __init__(self, entity, score=0.0):
        """构造函数

        Arguments:
            entity {str} --  实体的名称，在图谱中是唯一的
        """

        self.entity = entity
        # 这个候选项的得分
        self.score = score

    def __hash__(self):
        return hash(self.entity)

    def __eq__(self, value):
        """重载==，判断依据entity是否相等
        """
        if isinstance(value, Candidate):
            if self.entity == value.entity:
                return True
            else:
                return False
        else:
            return False
