import threading

import entitylinking.jieba as jieba
from ..base.mention import Mention

from ..config.app_config import AppConfig


class DictNER:
    """基于词典的mention识别
    """

    _clock = threading.Lock()

    @classmethod
    def instance(cls):
        """过去单实例
        """
        if not hasattr(cls, '_instance'):
            with cls._clock:
                dic_file = AppConfig.instance().mention_dic
                cls._instance = DictNER(dic_file)
                return cls._instance
        else:
            return cls._instance

    def __init__(self, dic_file):
        """dic_file文件的词典是由tab分割
        """
        self._entity_dict = {}
        self._load_dic_file(dic_file)

    def get_mentions(self, text):
        """从text中识别词典中的词
        """
        words = jieba.tokenize(text, cut_all=False)

        mentions = []
        for word, start, end in words:
            if word in self._entity_dict:
                mention = Mention(start, end - start, word)
                mentions.append(mention)

        return mentions

    def _load_dic_file(self, dic_file):
        """加载词典文件
        """
        with open(dic_file, mode='r', encoding='utf-8') as f:
            for line in f:
                fields = line.split('\t')
                if len(fields) >= 1:
                    key = fields[0].strip()
                    self._entity_dict[key] = fields[1:]
