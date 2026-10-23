import pytest

from app.search.index import InvertedIndex


@pytest.fixture
def index():
    idx = InvertedIndex()

    idx.add_document(3, "storm rain")
    idx.add_document(1, "cyclone strong cyclone")
    idx.add_document(2, "cyclone storm")

    return idx


def test_add_document_and_postings(index):
    assert index.postings("cyclone") == {1: 2, 2: 1}
    assert index.postings("storm") == {2: 1, 3: 1}


def test_unknown_term_returns_empty_dictionary(index):
    assert index.postings("earthquake") == {}


def test_search_and(index):
    assert index.search_and("cyclone storm") == [2]


def test_search_or(index):
    assert index.search_or("cyclone storm") == [1, 2, 3]


def test_search_results_are_sorted(index):
    assert index.search_or("storm cyclone") == [1, 2, 3]


def test_search_with_no_valid_terms(index):
    assert index.search_and("the and is") == []
    assert index.search_or("the and is") == []


def test_document_statistics(index):
    assert index.doc_count == 3
    assert index.doc_length(1) == 3
    assert index.doc_length(2) == 2
    assert index.doc_length(3) == 2
    assert index.avg_doc_length == pytest.approx(7 / 3)


def test_remove_document(index):
    index.remove_document(2)

    assert index.doc_count == 2
    assert index.postings("cyclone") == {1: 2}
    assert index.postings("storm") == {3: 1}
    assert index.doc_length(2) == 0


def test_replacing_document_updates_index(index):
    index.add_document(1, "rain rain")

    assert index.postings("cyclone") == {2: 1}
    assert index.postings("strong") == {}
    assert index.postings("rain") == {1: 2, 3: 1}
    assert index.doc_length(1) == 2
    assert index.doc_count == 3


def test_removing_unknown_document_is_safe(index):
    index.remove_document(99)

    assert index.doc_count == 3
    assert index.search_or("cyclone") == [1, 2]


def test_empty_index_statistics():
    idx = InvertedIndex()

    assert idx.doc_count == 0
    assert idx.avg_doc_length == 0.0
    assert idx.doc_length(99) == 0