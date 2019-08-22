import os

import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer

from ..utils.file_utils import get_files
from .lucene_helper import init_lucene
from .lucene_helper import SUBJECT_FIELD,OBJECT_FIELD,PREDICATE_FIELD


def triple_index_create(data, index_dir):
    """构建三元组索引

    Arguments:
        data {str} -- 要构建索引的cn-dbpedia数据目录或者单个文件
        index_dir {str} -- 索引存放的目录
    """
    writer = _create_index_writer(index_dir)
    _write_documents(writer, data)
    writer.commit()
    writer.close()


def _create_index_writer(index_dir):
    """构建lucene索引的index writer，用于写入document

    Arguments:
        index_dir {str} -- 索引的目录

    Returns:
        IndexWriter -- lucene的IndexWriter
    """
    init_lucene()
    directory = MMapDirectory(Paths.get(index_dir))
    analyzer = SmartChineseAnalyzer()
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(directory, config)
    return writer


def _write_documents(writer, data_dir):
    """将data_dir目录下的三元组文件写入到writer中。
    三元组数据文件的格式是以tab分割的SPO。
    """
    files = get_files(data_dir)
    for file in files:
        with open(file, mode='r', encoding="utf-8") as f:
            for line in f:
                fields = line.split('\t')
                if len(fields) == 3:
                    doc = Document()
                    doc.add(
                        Field(SUBJECT_FIELD, fields[0], StringField.TYPE_STORED))
                    doc.add(Field(PREDICATE_FIELD,
                                  fields[1], StringField.TYPE_STORED))
                    doc.add(
                        Field(OBJECT_FIELD, fields[2], StringField.TYPE_STORED))
                    writer.addDocument(doc)
