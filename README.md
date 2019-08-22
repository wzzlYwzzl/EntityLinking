# EntityLinking

中文知识图谱实体链接服务。

## 关于内部jieba的说明

为了方便按照需求改造jieba，所以项目中直接将jieba的源码作为了项目内的一个module。

对原始的jieba做了如下的修改：

1. 在init文件中修改re_han_default，添加了空格、/、<、>。
2. 自定义词典改成用tab作为分隔，以支持英文自定义词典。
