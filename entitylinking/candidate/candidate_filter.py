class CandidateFilter:
    """过滤一个mention的candidates。
    这是一个基类。
    """

    def filter(self, doc, mention, candidates):
        """每个CandidateFilter必须要实现的方法。
        
        Arguments:
            doc {Document} -- 含有用户输入的要进行实体链接的文本信息
            mention {Mention} -- 需要实体链接的指称项
            candidates {list<Candidate>} -- mention的候选实体
        """
        pass