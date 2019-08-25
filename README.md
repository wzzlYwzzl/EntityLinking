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

## 出现的错误

...
完成34690000行，耗时18036.621724200002
完成34700000行，耗时18043.1189176
完成34710000行，耗时18046.7838767
完成34720000行，耗时18053.1160476
完成34730000行，耗时18056.683092
完成34740000行，耗时18060.2204738
Traceback (most recent call last):
  File "D:\anaconda\lib\site-packages\whoosh\util\numlists.py", line 57, in append
    self.array.append(n)
OverflowError: Python int too large to convert to C unsigned long

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "index_create.py", line 10, in <module>
    triple_index_create(data, index_dir)
  File "E:\PythonCodes\EntityLinking\entitylinking\index_whoosh\triple_index_creator.py", line 31, in triple_index_create
    _create_triple_index(storage, data)
  File "E:\PythonCodes\EntityLinking\entitylinking\index_whoosh\triple_index_creator.py", line 44, in _create_triple_index
    _write_document(writer, data)
  File "E:\PythonCodes\EntityLinking\entitylinking\index_whoosh\triple_index_creator.py", line 82, in _write_document
    object=fields[2].strip()
  File "D:\anaconda\lib\site-packages\whoosh\writing.py", line 786, in add_document
    perdocwriter.finish_doc()
  File "D:\anaconda\lib\site-packages\whoosh\codec\whoosh3.py", line 250, in finish_doc
    self.add_column_value("_stored", STORED_COLUMN, sf)
  File "D:\anaconda\lib\site-packages\whoosh\codec\base.py", line 821, in add_column_value
    self._get_column(fieldname).add(self._docnum, value)
  File "D:\anaconda\lib\site-packages\whoosh\columns.py", line 1265, in add
    self._child.add(docnum, v)
  File "D:\anaconda\lib\site-packages\whoosh\columns.py", line 855, in add
    VarBytesColumn.Writer.add(self, docnum, v)
  File "D:\anaconda\lib\site-packages\whoosh\columns.py", line 276, in add
    self._offsets.append(self._offset_base)
  File "D:\anaconda\lib\site-packages\whoosh\util\numlists.py", line 59, in append
    self._retype(n)
  File "D:\anaconda\lib\site-packages\whoosh\util\numlists.py", line 48, in _retype
    raise OverflowError("%r is too big to fit in an array" % maxnum)
OverflowError: 4294967357 is too big to fit in an array
