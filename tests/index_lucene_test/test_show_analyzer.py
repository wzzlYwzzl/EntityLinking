import pytest

from entitylinking.index_lucene.analyzer_utils import \
    show_analyzer_result, get_cn_master_analyzer, \
        get_stardard_analyzer


@pytest.mark.analyzer
def test_show_analyzer():
    text = '我是中国人'
    analyzer = get_cn_master_analyzer()
    show_analyzer_result(analyzer, text)

    analyzer = get_stardard_analyzer()
    show_analyzer_result(analyzer, text)
    assert True