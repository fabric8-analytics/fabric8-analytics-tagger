"""Tests for functions from recipes module."""

import pytest
from unittest.mock import *
from f8a_tagger.errors import InvalidInputError
import f8a_tagger.recipes


def test_get_registered_stemmers():
    """Test for the function get_registered_stemmers()."""
    stemmers = f8a_tagger.recipes.get_registered_stemmers()
    assert stemmers
    assert len(stemmers) >= 3


def test_get_registered_scorers():
    """Test for the function get_registered_scorers()."""
    scorers = f8a_tagger.recipes.get_registered_scorers()
    assert scorers
    # ['Count', 'RelativeUsage', 'TfIdf']
    assert len(scorers) >= 3


def test_get_registered_collectors():
    """Test for the function get_registered_collectors()."""
    collectors = f8a_tagger.recipes.get_registered_collectors()
    assert collectors
    # ['Maven', 'NPM', 'PyPI', 'StackOverflow']
    assert len(collectors) >= 4


def test_reckon():
    """Test for the function reckon()."""
    result = f8a_tagger.recipes.reckon()
    assert "keywords" in result
    assert "stopwords" in result


@patch('f8a_tagger.tokenizer.Tokenizer.tokenize', return_value=["token1", "token2", "token3"])
def test_lookup_text(_mocked_function):
    """Test for the function lookup_text()."""
    score = f8a_tagger.recipes.lookup_text("Hello world")
    assert not score

    # test the check in the function
    with pytest.raises(InvalidInputError) as e:
        f8a_tagger.recipes.lookup_text(None)


@patch('f8a_tagger.tokenizer.Tokenizer.tokenize', return_value=["token1", "token2", "token3"])
def test_lookup_file(_mocked_function):
    """Test for the function lookup_file()."""
    result = f8a_tagger.recipes.lookup_file("test_data/README_rst.json", ignore_errors=True)
    result = f8a_tagger.recipes.lookup_file("test_data/README_rst.json")

    with pytest.raises(ValueError):
        result = f8a_tagger.recipes.lookup_file("test_data/")

    # check the logging error part
    result = f8a_tagger.recipes.lookup_file("test_data/", ignore_errors=True)

    # check the logging error part
    result = f8a_tagger.recipes.lookup_file("http://google.com", ignore_errors=True)


@patch('f8a_tagger.tokenizer.Tokenizer.tokenize', return_value=["token1", "token2", "token3"])
def test_lookup_readme_proper_input(_mocked_function):
    """Test for the function lookup_readme()."""
    payload = {
        "type": "reStructuredText",
        "content": "Hello world!"
    }
    results = f8a_tagger.recipes.lookup_readme(payload)


def test_lookup_readme_wrong_input():
    """Test for the function lookup_readme()."""
    with pytest.raises(InvalidInputError) as e:
        f8a_tagger.recipes.lookup_readme(None)

    # empty dictionary
    payload = {
    }
    with pytest.raises(InvalidInputError) as e:
        f8a_tagger.recipes.lookup_readme(payload)

    # missing 'content' attribute
    payload = {
        "type": "reStructuredText"
    }
    with pytest.raises(InvalidInputError) as e:
        f8a_tagger.recipes.lookup_readme(payload)

    # missing 'type' attribute
    payload = {
        "content": "Hello world!"
    }
    with pytest.raises(InvalidInputError) as e:
        f8a_tagger.recipes.lookup_readme(payload)


def test_prepare_lookup():
    """Test for the function _prepare_lookup()."""
    ngram_size, tokenizer, chief, parser = f8a_tagger.recipes._prepare_lookup(
        keywords_file="test_data/keywords.yaml")
    assert ngram_size > 0

    ngram_size, tokenizer, chief, parser = f8a_tagger.recipes._prepare_lookup(
        keywords_file="test_data/keywords.yaml", ngram_size=1000)
    assert ngram_size > 0

    ngram_size, tokenizer, chief, parser = f8a_tagger.recipes._prepare_lookup(
        keywords_file="test_data/keywords.yaml", ngram_size=0)
    assert ngram_size == 0


@patch('f8a_tagger.tokenizer.Tokenizer.tokenize', return_value=["token1", "token2", "token3"])
def test_perform_lookup(_mocked_function):
    """Test for the function _perform_lookup()."""
    ngram_size, tokenizer, chief, parser = f8a_tagger.recipes._prepare_lookup(
        keywords_file="test_data/keywords.yaml")
    score = f8a_tagger.recipes._perform_lookup("hello world", tokenizer, chief, None)
    assert not score


def test_aggregate():
    """Test for the function aggregate()."""
    with pytest.raises(ValueError):
        f8a_tagger.recipes.aggregate(None)

    keywords = f8a_tagger.recipes.aggregate(["test_data/keywords.yaml"])
    assert "python" in keywords
    assert "machine-learning" in keywords

    keywords = f8a_tagger.recipes.aggregate(["test_data/keywords.yaml"],
                                            occurrence_count_filter=1)
    assert "python" in keywords
    assert "machine-learning" in keywords

    keywords = f8a_tagger.recipes.aggregate(["test_data/keywords.yaml"],
                                            occurrence_count_filter=2)
    assert keywords == {}

    keywords = f8a_tagger.recipes.aggregate(["test_data/keywords.yaml", "test_data/keywords.yaml"],
                                            occurrence_count_filter=1)
    assert "python" in keywords
    assert "machine-learning" in keywords

    # special file with keyword that does not matches
    keywords = f8a_tagger.recipes.aggregate(["test_data/keywords_does_not_match.yaml"])
    assert keywords == {}


def test_collect():
    """Test for the function collect()."""
    with pytest.raises(Exception) as e:
        f8a_tagger.recipes.collect()


if __name__ == '__main__':
    test_get_registered_stemmers()
    test_get_registered_scorers()
    test_get_registered_collectors()
    test_reckon()
    test_lookup_text()
    test_lookup_file()
    test_lookup_readme_proper_input()
    test_lookup_readme_wrong_input()
    test_prepare_lookup()
    test_perform_lookup()
    test_aggregate()
    test_collect()
