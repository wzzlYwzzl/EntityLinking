class Mention:
    """用户输入文本中，指向图谱实体的词
    """

    def __init__(self, start_pos, length, word, mention_type):
        # mention的word在用户原始输入中的起始位置
        self.start_pos = start_pos

        # word的长度
        self.length = length

        # mention文本的内容
        self.word = word

        # 类别，比如people、company等等
        self.mention_type = mention_type
        
        #word的结束位置
        self.end_pos = start_pos + length
