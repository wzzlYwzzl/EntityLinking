# EntityLinking

中文知识图谱实体链接服务。

## 关于内部jieba的说明

为了方便按照需求改造jieba，所以项目中直接将jieba的源码作为了项目内的一个module。

对原始的jieba做了如下的修改：

1. 在init文件中修改re_han_default，添加了空格、/、<、>。
2. 自定义词典改成用tab作为分隔，以支持英文自定义词典。
3. 修改了tokenize方法对于mode=search时的分词
4. 修改了cut中cut_all的bug

```python
import whoosh.index as index
import whoosh.qparser as qparser
from whoosh.qparser import QueryParser

import sys
sys.path.append('/Users/caoxiaojie/pythonCode/EntityLinking')

index_dir = '/Users/caoxiaojie/pythonCode/EntityLinking/data/index_all'
ix = index.open_dir(index_dir, indexname='triple')
s = ix.searcher()
qp = QueryParser('subject',schema=ix.schema,group=qparser.OrGroup)
qp2 = QueryParser('subject',schema=ix.schema)

q = qp.parse(u'subject:(李娜) AND object:(唱歌的)')

results = s.search(q, limit=20)

for r in results:
    print(r['subject'])

```
