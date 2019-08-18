class Document:
    """表示用于进行实体链接的文本。
    可能是输入的一句话，也可能是一篇文章。
    其中包含了要链接的mention。
    """

    def __init__(self, text):
        # 原始文本
        self.text = text
        # text中的mentions
        self.mention_list = []
