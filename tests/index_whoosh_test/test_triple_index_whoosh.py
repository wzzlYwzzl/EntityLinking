import pytest


@pytest.mark.whoosh_triple_search
def test_triple_search(triple_index):
    triples = triple_index.search(subject='再也不见')
    assert len(triples) != 0
