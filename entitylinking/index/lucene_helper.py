import lucene

# 全局的标识，标识是否已经调用过了lucene.initVM函数
lucene_vm_init = False

SUBJECT_FIELD = "subject"
PREDICATE_FIELD = "predicate"
OBJECT_FIELD = "object"


def init_lucene():
    """初始化lucene模块，所有使用lucene的其他代码都在初始化时
    调用这个方法，由这个方法保证不会出现多次的重复调用。
    """
    global lucene_vm_init
    if not lucene_vm_init:
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        lucene_vm_init = True
