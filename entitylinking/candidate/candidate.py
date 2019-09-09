class Candidate:
    """标识mention的一个候选实体
    """

    def __init__(self, entity=None, id=None, score=0.0):
        """构造函数

        Arguments:
            entity {str} --  实体的名称，在图谱中是唯一的
        """

        self.entity = entity
        # 这个候选项的得分
        self.score = score

        # id表示entity的唯一标识，如果不赋值，那么就是entity
        if id:
            self.id = id
        else:
            self.id = entity

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, value):
        """重载==，判断依据entity是否相等
        """
        if isinstance(value, Candidate):
            if self.id == value.id:
                return True
            else:
                return False
        else:
            return False
