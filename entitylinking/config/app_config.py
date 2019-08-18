import threading


class AppConfig:
    """关于整个entity linking服务的配置信息，
    主要从应用的配置文件中加载得到。
    """

    _instance_lock = threading.Lock()

    @classmethod
    def init_instance(cls, config_file):
        """根据配置文件来初始化配置。配置文件格式如下：
        注释：以#开始
        配置：key=value，key表示配置变量名，value表示配置的取值

        Arguments:
            config_file -- 配置文件
        """
        with AppConfig._instance_lock:
            AppConfig._instance = AppConfig(config_file)

    @classmethod
    def instance(cls):
        """AppConfig配置类的实例
        """
        if not hasattr(AppConfig, '_instance'):
            raise Exception("获取instance之前，必须调用init_instance方法")
        return AppConfig._instance

    def __init__(self, config_file):
        """构造函数

        Argments：
            config_file -- 配置文件
        """
        # 用于存放key=value的属性
        self._properties_map = {}

        with open(config_file, mode='r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    continue

                fields = line.split('=')
                if len(fields) == 2:
                    key = fields[0].strip()
                    value = fields[1].strip()
                    self._properties_map[key] = value

    def __getattr__(self, name):
        """使配置文件中的key=value通过属性的方式访问
        """
        if name in self._properties_map:
            return self._properties_map[name]
        else:
            raise Exception("配置文件没有配置项：{}".format(name))
