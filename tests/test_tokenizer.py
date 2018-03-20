"""Tests for the Tokenizer class."""

import pytest
import io
from f8a_tagger.tokenizer import Tokenizer
from f8a_tagger.errors import InvalidInputError


def test_initial_state():
    """Check the initial state of Tokenizer."""
    tokenizer = Tokenizer(None, None)
    assert tokenizer


def test_stopwords_reading():
    """Check the ability to read stopwords."""
    with open("test_data/stopwords.txt", "r") as fin:
        content = fin.read()
        bytestream = io.BytesIO(content.encode())
        fin = io.TextIOWrapper(bytestream)
        tokenizer = Tokenizer(fin, None)
        assert tokenizer

    with open("test_data/stopwords_bad_re.txt", "r") as fin:
        content = fin.read()
        bytestream = io.BytesIO(content.encode())
        fin = io.TextIOWrapper(bytestream)
        tokenizer = Tokenizer(fin, None)
        assert tokenizer

    with pytest.raises(InvalidInputError) as e:
        tokenizer = Tokenizer({}, None)


def test_raw_stopwords_property():
    """Check the raw_stopwords property."""
    tokenizer = Tokenizer("test_data/stopwords.txt", None)
    stopwords = tokenizer.raw_stopwords
    assert stopwords
    expected = {"i", "me", "our", "he", "she"}
    # subset operation
    assert expected <= set(stopwords)


def test_regexp_stopwords_property():
    """Check the regexp_stopwords property."""
    tokenizer = Tokenizer("test_data/stopwords.txt", None)
    stopwords = tokenizer.regexp_stopwords
    assert stopwords
    assert "re: [0-9.]+" in stopwords


def test_remove_stopwords_method():
    """Check the remove_stopwords method."""
    tokenizer = Tokenizer("test_data/stopwords.txt", None)

    stopwords = tokenizer.raw_stopwords
    assert stopwords
    expected = {"i", "me", "our", "he", "she"}
    assert expected <= set(stopwords)

    # remove some stopwords and check again
    stopwords = tokenizer.remove_stopwords(["foo", "something", "me", "our", "bar"])
    expected = {"foo", "bar"}
    assert expected == set(stopwords)

    # remove some stopwords and check again
    stopwords = tokenizer.remove_stopwords(["foo", "0", "123", "6502", "bar"])
    print(stopwords)
    expected = {"foo", "bar"}
    assert expected == set(stopwords)

    # remove some stopwords and check again
    stopwords = tokenizer.remove_stopwords(["foo", "-0", "-123", "-6502", "bar"])
    print(stopwords)
    expected = {"foo", "bar", "-0", "-123", "-6502"}
    assert expected == set(stopwords)


if __name__ == '__main__':
    test_initial_state()
    test_stopwords_reading()
    test_raw_stopwords_property()
    test_regexp_stopwords_property()
    test_remove_stopwords_method()
