class Mention:
    """用户输入文本中，指向图谱实体的词
    """

    def __init__(self, start_pos, length, word, mention_type=None):
        # mention的word在用户原始输入中的起始位置
        self.start_pos = start_pos

        # word的长度
        self.length = length

        # mention文本的内容
        self.word = word

        # 类别，比如people、company等等
        self.mention_type = mention_type

        # word的结束位置
        self.end_pos = start_pos + length

        # mention的上下文字符串，也就是用户输入问句中
        # 与mention词相连的上下文信息
        self.context = []

        # 当前的Mention所有的候选项
        self.candidates = []

    def context_str(self, join_str=''):
        """获取字符拼接的context

        Arguments:
            join_str {str} -- 用于拼接的字符串
        """
        return join_str.join(self.context)

    def link_result(self):
        """与当前mention匹配得分最高的candidate
        """
        ret = None
        if len(self.candidates) > 0:
            self.candidates.sort(key=lambda item: item.score, reverse=True)
            ret = self.candidates[0]
        return ret

    def sort_candidates(self):
        """对候选项进行排序
        """
        self.candidates.sort(key=lambda item: item.score, reverse=True)

    def __hash__(self):
        return hash(self.word + str(self.start_pos))

    def __eq__(self, value):
        if isinstance(value, Mention):
            if value.word == self.word and value.start_pos == self.start_pos:
                return True
            else:
                return False
        else:
            return False
