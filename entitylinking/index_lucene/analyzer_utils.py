import lucene

from java.io import StringReader
from org.apache.lucene.analysis import Analyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
from org.apache.lucene.analysis import TokenStream
from org.apache.lucene.analysis.tokenattributes import \
    OffsetAttribute, CharTermAttribute, TypeAttribute, \
    PositionIncrementAttribute

from .lucene_helper import init_lucene


def show_analyzer_result(analyzer, text):
    """展示lucene的Analyzer处理text的结果
    """
    init_lucene()
    str_reader = StringReader(text)
    token_stream = analyzer.tokenStream("context,", str_reader)
    attr = token_stream.addAttribute(CharTermAttribute.class_)
    token_stream.reset()
    while token_stream.incrementToken():
        print(attr.toString())

    token_stream.end()
    token_stream.close()


def get_cn_master_analyzer():
    """获取SmartChineseAnalyzer的实例
    """
    init_lucene()
    analyzer = SmartChineseAnalyzer()
    return analyzer

def get_stardard_analyzer():
    """获取StandardAnalyzer实例
    """
    init_lucene()
    analyzer = StandardAnalyzer()
    return analyzer