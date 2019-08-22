import os
import threading

from ..config.app_config import AppConfig
from ..candidate.candidate import Candidate


class CandidateUtils:
    """根据mention获取候选实体
    """

    _lock = threading.Lock()

    @classmethod
    def instance(cls):
        if not hasattr(cls, '_instance'):
            with cls._lock:
                cls._instance = CandidateUtils()
            return cls._instance
        else:
            return cls._instance

    def __init__(self):
        self._m2e_file = AppConfig.instance().m2e
        self._m2e_dic = {}
        self.load_m2e()

    def get_condidates(self, mention):
        """根据mention获取候选实体

        Arguments:
            mention {Mention} -- 表示一个mention的class

        Returns:
            list<Candidate> -- 候选项列表，如果没有就返回空list
        """
        if mention.word in self._m2e_dic:
            return self._m2e_dic[mention.word]
        else:
            # 这里暂时只从m2e的配置文件中获取，后面可以考虑通过搜索等其他
            # 手段处理。
            return []

    def load_m2e(self):
        """加载mention与候选实体的对应关系文件。
        文件的格式约定如下：
        mention+tab+entity
        也就是用tab分割mention和候选实体
        """
        m2e_file = self._m2e_file
        if not os.path.exists(m2e_file):
            return
        with open(m2e_file, mode='r', encoding='utf8') as f:
            for line in f:
                fields = line.strip().split('\t')
                if len(fields) == 2:
                    mention = fields[0].strip()
                    entity = fields[1].strip()
                    if mention in self._m2e_dic:
                        entity_list = self._m2e_dic[mention]
                        entity_list.append(Candidate(entity))
                    else:
                        entity_list = []
                        entity_list.append(Candidate(entity))
                        self._m2e_dic[mention] = entity_list
