"""Tests for the KeywordsChief class."""

import pytest
from f8a_tagger.keywords_chief import KeywordsChief
import f8a_tagger.defaults as defaults
import f8a_tagger.errors


def test_initial_state():
    """Check the initial state of KeywordsChief."""
    pass


def test_custom_keyword_file_loading():
    """Test if the custom keyword file could be loaded."""
    pass


def test_non_existing_keyword_file_loading():
    """Test if non-existing keyword file is properly reported."""
    pass


def test_keyword_file_check():
    """Test the checks performed over keyword file."""
    pass


def test_keywords_property():
    """Check the 'keywords' property."""
    pass


def test_get_keywords_count_method():
    """Check the get_keywords_count() method."""
    pass


def test_get_average_occurence_count_method():
    """Check the get_average_occurrence_count() method."""
    pass


def test_compute_ngram_size_method():
    """Check the compute_ngram_size() method."""
    pass


def test_get_keyword_method_positive():
    """Check the get_keyword() method."""
    pass


def test_get_keyword_method_negative():
    """Check the get_keyword() method."""
    pass


def test_extract_keywords():
    """Test the method extract_keywords()."""
    pass


def test_filter_keywords():
    """Test the static method filter_keyword()."""
    pass


def test_compute_synonyms():
    """Test the static method compute_synonyms()."""
    pass


def test_is_keyword_positive():
    """Test the method/predicate is_keyword()."""
    pass


def test_is_keyword_negative():
    """Test the method/predicate is_keyword()."""
    pass


def test_matches_keyword_pattern_positive():
    """Test the class method matches_keyword_pattern()."""
    pass


def test_matches_keyword_pattern_negative():
    """Test the class method matches_keyword_pattern()."""
    pass


if __name__ == '__main__':
    test_initial_state()
    test_custom_keyword_file_loading()
    test_non_existing_keyword_file_loading()
    test_keyword_file_check()
    test_keywords_property()
    test_get_keywords_count_method()
    test_get_average_occurence_count_method()
    test_compute_ngram_size_method()
    test_get_keyword_method_positive()
    test_get_keyword_method_negative()
    test_extract_keywords()
    test_filter_keywords()
    test_compute_synonyms()
    test_is_keyword_positive()
    test_is_keyword_negative()
    test_matches_keyword_pattern_positive()
    test_matches_keyword_pattern_negative()
