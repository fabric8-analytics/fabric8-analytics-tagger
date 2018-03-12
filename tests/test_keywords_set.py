"""Tests for the KeywordsSet class."""

import pytest
from f8a_tagger.keywords_set import KeywordsSet


def test_initial_state():
    """Check the initial state of KeywordsSet."""
    ks = KeywordsSet()
    assert ks.keywords == {}


def test_add_method():
    """Check the method KeywordsSet.add()."""
    ks = KeywordsSet()
    assert ks.keywords == {}

    # first keyword
    ks.add("keyword")
    assert "keyword" in ks.keywords
    assert "occurrence_count" in ks.keywords["keyword"]
    assert ks.keywords["keyword"]["occurrence_count"] == 1

    # second keyword
    ks.add("keyword2", 42)

    # check the firts and the second keyword as well
    assert "keyword2" in ks.keywords
    assert "occurrence_count" in ks.keywords["keyword"]
    assert ks.keywords["keyword"]["occurrence_count"] == 1
    assert "keyword2" in ks.keywords
    assert "occurrence_count" in ks.keywords["keyword2"]
    assert ks.keywords["keyword2"]["occurrence_count"] == 42


def test_occurrence_counting():
    """Check occurrence counting."""
    ks = KeywordsSet()
    ks.add("keyword")
    assert ks.keywords["keyword"]["occurrence_count"] == 1
    ks.add("keyword")
    assert ks.keywords["keyword"]["occurrence_count"] == 2
    ks.add("keyword", 10)
    assert ks.keywords["keyword"]["occurrence_count"] == 12


def test_union_method():
    """Check the method KeywordsSet.union()."""
    ks1 = KeywordsSet()
    ks1.add("keyword1")

    ks2 = KeywordsSet()
    ks2.add("keyword2")

    # pre-operation checks
    assert "keyword1" in ks1.keywords
    assert "keyword2" not in ks1.keywords

    assert "keyword1" not in ks2.keywords
    assert "keyword2" in ks2.keywords

    ks1.union(ks2)
    # post-operation checks
    assert "keyword1" in ks1.keywords
    assert "keyword2" in ks1.keywords

    assert "keyword1" not in ks2.keywords
    assert "keyword2" in ks2.keywords


def test_union_method_and_occurrence_count_1():
    """Check the method KeywordsSet.union() and occurrence count."""
    ks1 = KeywordsSet()
    ks1.add("keyword1")

    ks2 = KeywordsSet()
    ks2.add("keyword2")

    # pre-operation checks
    assert "keyword1" in ks1.keywords
    assert "keyword2" not in ks1.keywords
    assert ks1.keywords["keyword1"]["occurrence_count"] == 1

    assert "keyword1" not in ks2.keywords
    assert "keyword2" in ks2.keywords
    assert ks2.keywords["keyword2"]["occurrence_count"] == 1

    ks1.union(ks2)
    # post-operation checks
    assert "keyword1" in ks1.keywords
    assert "keyword2" in ks1.keywords
    assert ks1.keywords["keyword1"]["occurrence_count"] == 1
    assert ks1.keywords["keyword2"]["occurrence_count"] == 1

    assert "keyword1" not in ks2.keywords
    assert "keyword2" in ks2.keywords


def test_union_method_and_occurrence_count_2():
    """Check the method KeywordsSet.union() and occurrence count."""
    ks1 = KeywordsSet()
    ks1.add("keyword1", 10)

    ks2 = KeywordsSet()
    ks2.add("keyword2", 20)

    # pre-operation checks
    assert "keyword1" in ks1.keywords
    assert "keyword2" not in ks1.keywords
    assert ks1.keywords["keyword1"]["occurrence_count"] == 10

    assert "keyword1" not in ks2.keywords
    assert "keyword2" in ks2.keywords
    assert ks2.keywords["keyword2"]["occurrence_count"] == 20

    ks1.union(ks2)
    # post-operation checks
    assert "keyword1" in ks1.keywords
    assert "keyword2" in ks1.keywords
    assert ks1.keywords["keyword1"]["occurrence_count"] == 10
    assert ks1.keywords["keyword2"]["occurrence_count"] == 20

    assert "keyword1" not in ks2.keywords
    assert "keyword2" in ks2.keywords


def test_union_method_for_overlapping_data():
    """Check the method KeywordsSet.union() for overlapping data."""
    ks1 = KeywordsSet()
    ks1.add("keyword", 10)

    ks2 = KeywordsSet()
    ks2.add("keyword", 20)

    # pre-operation checks
    assert "keyword" in ks1.keywords
    assert "keyword" in ks1.keywords
    assert ks1.keywords["keyword"]["occurrence_count"] == 10
    assert ks2.keywords["keyword"]["occurrence_count"] == 20

    ks1.union(ks2)
    # post-operation checks
    assert "keyword" in ks1.keywords
    assert ks1.keywords["keyword"]["occurrence_count"] == 10


if __name__ == '__main__':
    test_initial_state()
    test_add_method()
    test_occurrence_counting()
    test_union_method()
    test_union_method_and_occurrence_count_1()
    test_union_method_and_occurrence_count_2()
    test_union_method_for_overlapping_data()
