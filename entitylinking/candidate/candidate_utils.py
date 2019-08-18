import threading


class CandidateUtils:
    """根据mention获取候选实体
    """

    _lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def get_condidates(self, mention):
        """根据mention获取候选实体

        Returns:
            list<Candidate> -- 候选项列表
        """
        pass
