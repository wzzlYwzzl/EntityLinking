from ..base.mention import Mention
from ..ner.dict_ner import DictNER
import entitylinking.jieba as jieba


stop_words = {
    '的', '是', '了', '和', '地', '得', '在', '这', '吗', '呢', '啊', '不', '不是'
}


class Document:
    """表示用于进行实体链接的文本。
    可能是输入的一句话，也可能是一篇文章。
    其中包含了要链接的mention。
    """

    def __init__(self, origin_text, has_entity_tag=True):
        # 原始文本
        self.origin_text = origin_text
        # text中的mentions
        self.mention_list = []

        if has_entity_tag:
            # 除去<entity>和</entity>标签的文本
            self.text = origin_text.replace(
                '<entity>', '').replace('</entity>', '')
            self.text2doc()
        else:
            self.text = origin_text
            self.mention_list = DictNER.instance().get_mentions(self.text)
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
                context_words = self.process_context(
                    self.text[0:mention_cur.start_pos])
                mention_cur.context.append(''.join(context_words))
            else:
                mention_pre = self.mention_list[i-1]
                text_tmp = self.text[mention_pre.end_pos:mention_cur.start_pos]
                context_words = self.process_context(text_tmp)

                if mention_cur.word != mention_pre.word:
                    mention_pre.context.append(''.join(context_words))
                    mention_pre.context.append(mention_cur.word)
                    mention_cur.context.append(mention_pre.word)
                    mention_cur.context.append(''.join(context_words))
                else:
                    if len(mention_pre.context_str()) < 2:
                        half_a, half_b = self.sep_words(context_words)
                        mention_pre.context.append(half_a)
                        mention_cur.context.append(half_b)
                    else:
                        mention_cur.context.append(''.join(context_words))

            if i == length - 1:
                context_words = self.process_context(
                    self.text[mention_cur.end_pos:])
                mention_cur.context.append(''.join(context_words))

    def sort_candidates(self):
        """对candiate进行排序，根据score从大到小排序
        """
        for mention in self.mention_list:
            mention.sort_candidates()

    def process_context(self, context):
        """对context做分词处理，除去一些没价值的stopwords
        """
        words = jieba.cut_with_stopwords(context)
        return list(words)

    def sep_words(self, words_list):
        """将words_list划分为两份
        """
        half_a = []
        half_b = []
        l = len(words_list)
        if not l == 0:
            half = int(l / 2)
            if half == 0:
                half_a = words_list[0:1]
                half_b = words_list[0:1]
            else:
                half_a = words_list[0:half]
                half_b = words_list[half:]

        half_a_str = ''.join(half_a)
        half_b_str = ''.join(half_b)
        return half_a_str, half_b_str
