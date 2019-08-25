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
        self.add_mention_context()

    def text2doc(self):
        """将origin_text中标注的实体提取出来
        """
        if not self.origin_text:
            return

        tmp_text = ""
        end_pos = 0
        start_pos = 0
        start_pos = self.origin_text.find('<entity>', end_pos)
        while start_pos >= 0:
            tmp_text += self.origin_text[end_pos:start_pos]
            start_pos += 8  # <entity>表示的实体的开始位置
            end_pos = self.origin_text.find('</entity>', end_pos)
            word = self.origin_text[start_pos:end_pos]
            mention = Mention(len(tmp_text), len(word), word)
            self.mention_list.append(mention)
            tmp_text += word

            end_pos += 9
            start_pos = self.origin_text.find('<entity>', end_pos)

    def add_mention_context(self):
        """为mention添加上下文
        """
        self.mention_list.sort(key=lambda iterm: iterm.start_pos)

        length = len(self.mention_list)

        for i in range(length):
            mention_cur = self.mention_list[i]
            if i == 0:
                mention_cur.context.append(self.text[0:mention_cur.start_pos])
            else:
                mention_pre = self.mention_list[i-1]
                text_tmp = self.text[mention_pre.end_pos:mention_cur.start_pos]

                if mention_cur.word != mention_pre.word:
                    mention_pre.context.append(text_tmp)
                    mention_pre.context.append(mention_cur.word)
                    mention_cur.context.append(mention_pre.word)
                else:
                    if len(mention_pre.context_str()) < 2:
                        mention_pre.context.append(text_tmp)
                mention_cur.context.append(text_tmp)

            if i == length - 1:
                mention_cur.context.append(self.text[mention_cur.end_pos:])
