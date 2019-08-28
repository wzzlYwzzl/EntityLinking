import threading

from entitylinking.jieba import Tokenizer
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
        self.tokenizer = Tokenizer(dictionary=dic_file, split='\t')

    def get_mentions(self, text):
        """从text中识别词典中的词
        """
        words = self.tokenizer.cut_from_dict(text)

        mentions = []
        for word, start, end in words:
            mention = Mention(start, end - start, word)
            mentions.append(mention)

        return mentions
