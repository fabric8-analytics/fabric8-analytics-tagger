"""Tests for the KeywordsSet class."""

import pytest
from f8a_tagger.keywords_set import KeywordsSet


def test_initial_state():
    """Check the initial state of KeywordsSet."""
    keywordsSet = KeywordsSet()
    assert keywordsSet
    assert keywordsSet.keywords == {}


def test_add_method():
    """Check the method KeywordsSet.add()."""
    keywordsSet = KeywordsSet()
    assert keywordsSet
    assert keywordsSet.keywords == {}

    # first keyword
    keywordsSet.add("keyword")
    assert "keyword" in keywordsSet.keywords
    assert len(keywordsSet.keywords) == 1
    assert "occurrence_count" in keywordsSet.keywords["keyword"]
    assert keywordsSet.keywords["keyword"]["occurrence_count"] == 1

    # second keyword
    keywordsSet.add("keyword2", 42)

    # check the firts and the second keyword as well
    assert "keyword2" in keywordsSet.keywords
    assert len(keywordsSet.keywords) == 2
    assert "occurrence_count" in keywordsSet.keywords["keyword"]
    assert keywordsSet.keywords["keyword"]["occurrence_count"] == 1
    assert "keyword2" in keywordsSet.keywords
    assert "occurrence_count" in keywordsSet.keywords["keyword2"]
    assert keywordsSet.keywords["keyword2"]["occurrence_count"] == 42


def test_occurrence_counting():
    """Check occurrence counting."""
    keywordsSet = KeywordsSet()
    keywordsSet.add("keyword")
    assert keywordsSet.keywords["keyword"]["occurrence_count"] == 1
    keywordsSet.add("keyword")
    assert keywordsSet.keywords["keyword"]["occurrence_count"] == 2
    keywordsSet.add("keyword", 10)
    assert keywordsSet.keywords["keyword"]["occurrence_count"] == 12


def test_union_method():
    """Check the method KeywordsSet.union()."""
    keywordsSet1 = KeywordsSet()
    keywordsSet1.add("keyword1")

    keywordsSet2 = KeywordsSet()
    keywordsSet2.add("keyword2")

    # pre-operation checkeywordsSet
    assert len(keywordsSet1.keywords) == 1
    assert len(keywordsSet2.keywords) == 1

    assert "keyword1" in keywordsSet1.keywords
    assert "keyword2" not in keywordsSet1.keywords

    assert "keyword1" not in keywordsSet2.keywords
    assert "keyword2" in keywordsSet2.keywords

    keywordsSet1.union(keywordsSet2)
    # post-operation checkeywordsSet
    assert len(keywordsSet1.keywords) == 2
    assert len(keywordsSet2.keywords) == 1

    assert "keyword1" in keywordsSet1.keywords
    assert "keyword2" in keywordsSet1.keywords

    assert "keyword1" not in keywordsSet2.keywords
    assert "keyword2" in keywordsSet2.keywords


def test_union_method_and_occurrence_count_1():
    """Check the method KeywordsSet.union() and occurrence count."""
    keywordsSet1 = KeywordsSet()
    keywordsSet1.add("keyword1")

    keywordsSet2 = KeywordsSet()
    keywordsSet2.add("keyword2")

    # pre-operation checkeywordsSet
    assert "keyword1" in keywordsSet1.keywords
    assert "keyword2" not in keywordsSet1.keywords
    assert keywordsSet1.keywords["keyword1"]["occurrence_count"] == 1

    assert "keyword1" not in keywordsSet2.keywords
    assert "keyword2" in keywordsSet2.keywords
    assert keywordsSet2.keywords["keyword2"]["occurrence_count"] == 1

    keywordsSet1.union(keywordsSet2)
    # post-operation checkeywordsSet
    assert "keyword1" in keywordsSet1.keywords
    assert "keyword2" in keywordsSet1.keywords
    assert keywordsSet1.keywords["keyword1"]["occurrence_count"] == 1
    assert keywordsSet1.keywords["keyword2"]["occurrence_count"] == 1

    assert "keyword1" not in keywordsSet2.keywords
    assert "keyword2" in keywordsSet2.keywords


def test_union_method_and_occurrence_count_2():
    """Check the method KeywordsSet.union() and occurrence count."""
    keywordsSet1 = KeywordsSet()
    keywordsSet1.add("keyword1", 10)

    keywordsSet2 = KeywordsSet()
    keywordsSet2.add("keyword2", 20)

    # pre-operation checkeywordsSet
    assert "keyword1" in keywordsSet1.keywords
    assert "keyword2" not in keywordsSet1.keywords
    assert keywordsSet1.keywords["keyword1"]["occurrence_count"] == 10

    assert "keyword1" not in keywordsSet2.keywords
    assert "keyword2" in keywordsSet2.keywords
    assert keywordsSet2.keywords["keyword2"]["occurrence_count"] == 20

    keywordsSet1.union(keywordsSet2)
    # post-operation checkeywordsSet
    assert "keyword1" in keywordsSet1.keywords
    assert "keyword2" in keywordsSet1.keywords
    assert keywordsSet1.keywords["keyword1"]["occurrence_count"] == 10
    assert keywordsSet1.keywords["keyword2"]["occurrence_count"] == 20

    assert "keyword1" not in keywordsSet2.keywords
    assert "keyword2" in keywordsSet2.keywords


def test_union_method_for_overlapping_data():
    """Check the method KeywordsSet.union() for overlapping data."""
    keywordsSet1 = KeywordsSet()
    keywordsSet1.add("keyword", 10)

    keywordsSet2 = KeywordsSet()
    keywordsSet2.add("keyword", 20)

    # pre-operation checkeywordsSet
    assert "keyword" in keywordsSet1.keywords
    assert "keyword" in keywordsSet1.keywords
    assert keywordsSet1.keywords["keyword"]["occurrence_count"] == 10
    assert keywordsSet2.keywords["keyword"]["occurrence_count"] == 20

    keywordsSet1.union(keywordsSet2)
    # post-operation checkeywordsSet
    assert "keyword" in keywordsSet1.keywords
    assert keywordsSet1.keywords["keyword"]["occurrence_count"] == 10


def test_union_method_for_empty_data():
    """Check the method KeywordsSet.union() for empty data."""
    keywordsSet1 = KeywordsSet()

    keywordsSet2 = KeywordsSet()

    # pre-operation checkeywordsSet
    assert keywordsSet1.keywords == {}
    assert keywordsSet2.keywords == {}

    keywordsSet1.union(keywordsSet2)
    # post-operation checkeywordsSet
    assert keywordsSet1.keywords == {}
    assert keywordsSet2.keywords == {}


if __name__ == '__main__':
    test_initial_state()
    test_add_method()
    test_occurrence_counting()
    test_union_method()
    test_union_method_and_occurrence_count_1()
    test_union_method_and_occurrence_count_2()
    test_union_method_for_overlapping_data()
    test_union_method_for_empty_data()
