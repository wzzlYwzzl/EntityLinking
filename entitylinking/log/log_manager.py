import os
import logging
import logging.handlers
import threading

from ..config.app_config import AppConfig


class LogManager:
    """整个应用的单实例日志类
    """

    _lock = threading.Lock()

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                cls._instance = LogManager()
        else:
            return cls._instance

    def __init__(self):
        self._logger = logging.getLogger("entitylinking_logger")
        self._logger.setLevel(logging.DEBUG)

        self._stream_handler = logging.StreamHandler()
        self._stream_handler.setLevel(logging.DEBUG)
        self._stream_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

        self._logger.addHandler(self._stream_handler)

        self._log_file = AppConfig.instance().log_file
        self._log_level = self.get_log_level()
        dir_tmp = os.path.dirname(self._log_file)
        if not os.path.exists(dir_tmp):
            os.makedirs(dir_tmp)
        self._file_handler = logging.handlers.RotatingFileHandler(
            self._log_file,
            maxBytes=10*1024*1024,
            encoding='utf-8'
        )
        self._file_handler.setLevel(self._log_level)
        self._file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self._logger.addHandler(self._file_handler)

    def debug(self, message):
        self._logger.debug(message)

    def info(self, message):
        self._logger.info(message)

    def warning(self, message):
        self.warning(message)

    def error(self, message):
        self.error(message)

    def get_log_level(self):
        """根据配置文件获取日志级别
        """
        level_str = AppConfig.instance().log_level.lower()
        log_level = logging.INFO
        if level_str == "error":
            log_level = logging.ERROR
        elif level_str == "warn":
            log_level = logging.WARN
        elif level_str == "debug":
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        return log_level
