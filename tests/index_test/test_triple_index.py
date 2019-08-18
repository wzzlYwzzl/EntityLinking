import pytest


@pytest.mark.index_search
def test_triple_search(config_instance, triple_index):
    subject = '韩信'
    result = triple_index.search(subject=subject)
    print(result)
    assert True


@pytest.mark.index_fuzzy_search
def test_triple_fuzzy_search(config_instance, triple_index):
    subject = '绿色工程'
    result = triple_index.fuzzy_search(subject=subject)
    print(result)
    assert True
