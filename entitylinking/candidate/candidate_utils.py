import os
import threading

from ..config.app_config import AppConfig
from ..candidate.candidate import Candidate
from .search_score_filter import SearchScoreFilter
from ..log.log_manager import LogManager


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
        self._subject2id_file = AppConfig.instance().subject2id
        self._m2e_dic = {}
        self._id2subject = {}
        self.filters = []

        # 必须先加载subject_id
        self.load_subject_id()
        self.load_m2e()
        self.add_filters()

    def add_candidates(self, doc):
        """为doc添加候选实体
        """
        for mention in doc.mention_list:
            candidates = self.get_candidates(doc, mention)
            mention.candidates = candidates

    def get_candidates(self, doc, mention):
        """根据mention获取候选实体

        Arguments:
            doc {Document} -- mention所在的Document
            mention {Mention} -- 表示一个mention的class

        Returns:
            list<Candidate> -- 候选项列表，如果没有就返回空list
        """
        if mention.word in self._m2e_dic:
            candidates = self._m2e_dic[mention.word]
        else:
            # 这里暂时只从m2e的配置文件中获取，后面可以考虑通过搜索等其他
            # 手段处理。
            candidates = []
        for f in self.filters:
            candidates = f.filter(doc, mention, candidates)

        return candidates

    def load_subject_id(self):
        """加载mention与候选实体的对应关系文件。
        文件的格式约定如下：
        mention+tab+entity
        也就是用tab分割mention和候选实体
        """
        subject2id_file = self._subject2id_file
        if not os.path.exists(subject2id_file):
            LogManager.instance().error("subject2id文件不存在")
        with open(subject2id_file, mode='r', encoding='utf8') as f:
            for line in f:
                fields = line.strip().split('\t')
                if len(fields) == 2:
                    subject = fields[0].strip()
                    subject_id = int(fields[1].strip())
                    if subject_id not in self._id2subject:
                        self._id2subject[subject_id] = subject

    def load_m2e(self):
        """加载实体与id的对应关系文件。
        文件的格式约定如下：
        subject+tab+id
        也就是用tab分割mention和候选实体
        """
        m2e_file = self._m2e_file
        if not os.path.exists(m2e_file):
            LogManager.instance().error("m2e文件不存在")
        with open(m2e_file, mode='r', encoding='utf8') as f:
            for line in f:
                fields = line.strip().split('\t')
                if len(fields) == 2:
                    mention = fields[0].strip()
                    subject_id = int(fields[1].strip())
                    entity = self._id2subject[subject_id]
                    if mention in self._m2e_dic:
                        entity_list = self._m2e_dic[mention]
                        entity_list.append(Candidate(entity=entity, id=subject_id))
                    else:
                        entity_list = []
                        entity_list.append(Candidate(entity=entity, id=subject_id))
                        self._m2e_dic[mention] = entity_list

    def add_filters(self):
        """添加过滤器，后面考虑可配置化的过滤器
        """
        search_filter = SearchScoreFilter()
        self.filters.append(search_filter)
