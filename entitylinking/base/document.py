from ..base.mention import Mention


class Document:
    """表示用于进行实体链接的文本。
    可能是输入的一句话，也可能是一篇文章。
    其中包含了要链接的mention。
    """

    def __init__(self, origin_text):
        # 原始文本
        self.origin_text = origin_text
        # text中的mentions
        self.mention_list = []

        # 除去<entity>和</entity>标签的文本
        self.text = origin_text.replace(
            '<entity>', '').replace('</entity>', '')
        self.text2doc()

    def text2doc(self):
        """将origin_text中标注的实体提取出来
        """
        if not self.origin_text:
            return
        
        find_start = 0
        start_pos = self.origin_text.find('<entity>', find_start)
        while start_pos >= 0:
            start_pos += 8  # <entity>表示的实体的开始位置
            end_pos = self.origin_text.find('</entity>', find_start)
            word = self.origin_text[start_pos:end_pos]
            mention = Mention(start_pos, end_pos-start_pos, word)
            self.mention_list.append(mention)

            find_start = end_pos + 9
            start_pos = self.origin_text.find('<entity>', find_start)
