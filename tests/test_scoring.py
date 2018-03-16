"""Tests for the Scoring class."""

import pytest
from f8a_tagger.keywords_chief import KeywordsChief
from f8a_tagger.keywords_set import KeywordsSet
from f8a_tagger.scoring import *


def test_get_registered_scorers():
    """Test the class method get_registered_scorers."""
    scorers = Scoring.get_registered_scorers()
    assert scorers

    # 'Count', 'RelativeUsage', 'TfIdf'
    assert len(scorers) >= 3


def test_get_scoring():
    """Test the class method get_scoring()."""
    s = Scoring.get_scoring('Count')
    assert s

    with pytest.raises(Exception) as e:
        Scoring.get_scoring('Unknown')


def test_count_scoring():
    """Test the class CountScoring."""
    s = Scoring.get_scoring("Count")
    assert s

    keywordsChief = KeywordsChief()
    keywords = keywordsChief.extract_keywords(["python", "functional-programming"])
    score = s.score(keywordsChief, keywords)
    assert score["python"] == 1
    assert score["functional-programming"] == 1


def test_relative_usage_scoring():
    """Test the class RelativeUsageScoring."""
    s = Scoring.get_scoring("RelativeUsage")
    assert s

    keywordsChief = KeywordsChief()
    keywords = keywordsChief.extract_keywords(["python", "functional-programming"])
    score = s.score(keywordsChief, keywords)
    assert score["python"] == 0.5
    assert score["functional-programming"] == 0.5

    keywords = keywordsChief.extract_keywords(["python", "python", "functional-programming"])
    score = s.score(keywordsChief, keywords)
    assert score["python"] == 0.5
    assert score["functional-programming"] < 0.5


def test_tfid_scoring():
    """Test the class TfIdfScoring."""
    s = Scoring.get_scoring("TfIdf")
    assert s

    keywordsChief = KeywordsChief()
    keywords = keywordsChief.extract_keywords(["python", "functional-programming"])
    with pytest.raises(NotImplementedError) as e:
        s.score(keywordsChief, keywords)


def test_scoring_func():
    """Test the static method _scoring_func."""
    assert RelativeUsageScoring._scoring_func(0, 0, 1, 1000) == 0.0


if __name__ == '__main__':
    test_get_registered_scorers()
    test_get_scoring()
    test_count_scoring()
    test_relative_usage_scoring()
    test_tfid_scoring()
    test_scoring_func()
