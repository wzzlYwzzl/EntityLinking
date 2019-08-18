class Candidate:
    """标识mention的一个候选实体
    """

    def __init__(self, entity):
        """构造函数

        Arguments:
            entity {str} --  实体的名称，在图谱中是唯一的
        """

        self.entity = entity
