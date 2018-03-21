"""Tests for the Tokenizer class."""

import pytest
from unittest.mock import *

import io
from f8a_tagger.tokenizer import Tokenizer
from f8a_tagger.errors import InstallPrepareError
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
    expected = {"foo", "bar"}
    assert expected == set(stopwords)

    # remove some stopwords and check again
    stopwords = tokenizer.remove_stopwords(["foo", "-0", "-123", "-6502", "bar"])
    expected = {"foo", "bar", "-0", "-123", "-6502"}
    assert expected == set(stopwords)


class CustomLemmatizer(object):
    """Custom lemmatizer to be used by following test."""

    def __init__(self):
        """Initialize this dummy class."""
        pass

    def lemmatize(self, x):
        """Lemmatize one word by simply returning it."""
        return x


class CustomLemmatizer2(object):
    """Custom lemmatizer to be used by following test."""

    def __init__(self):
        """Initialize this dummy class."""
        pass

    def lemmatize(self, x):
        """Lemmatize one word by altering it."""
        return "*" + x


class CustomLemmatizer3(object):
    """Custom lemmatizer to be used by following test."""

    def __init__(self):
        """Initialize this dummy class."""
        pass

    def lemmatize(self, x):
        """Lemmatize one word by returning constant."""
        return "***"


def test_lemmatize_method():
    """Check the _lemmatize method."""
    tokenizer = Tokenizer("test_data/stopwords.txt", None)

    # test with no lemmatizer
    tokens = ["foo", "bar", "me", "your", "6502"]
    tokenizer._lemmatize(tokens)
    assert tokens == ["foo", "bar", "me", "your", "6502"]

    # test with custom lemmatizer
    tokenizer = Tokenizer("test_data/stopwords.txt", lemmatizer=CustomLemmatizer())
    tokens = ["foo", "bar", "me", "your", "6502"]
    tokenizer._lemmatize(tokens)
    assert tokens == ["foo", "bar", "me", "your", "6502"]

    # test with custom lemmatizer
    tokenizer = Tokenizer("test_data/stopwords.txt", lemmatizer=CustomLemmatizer2())
    tokens = ["foo", "bar", "me", "your", "6502"]
    tokenizer._lemmatize(tokens)
    assert tokens == ["*foo", "*bar", "*me", "*your", "*6502"]

    # test with custom lemmatizer
    tokenizer = Tokenizer("test_data/stopwords.txt", lemmatizer=CustomLemmatizer3())
    tokens = ["foo", "bar", "me", "your", "6502"]
    tokenizer._lemmatize(tokens)
    assert tokens == ["***", "***", "***", "***", "***"]


class CustomStemmer(object):
    """Custom stemmer to be used by following test."""

    def __init__(self):
        """Initialize this dummy class."""
        pass

    def stem(self, x):
        """Stem one word by simply returning it."""
        return x


class CustomStemmer2(object):
    """Custom stemmer to be used by following test."""

    def __init__(self):
        """Initialize this dummy class."""
        pass

    def stem(self, x):
        """Stem one word by altering it."""
        return "*" + x


class CustomStemmer3(object):
    """Custom stemmer to be used by following test."""

    def __init__(self):
        """Initialize this dummy class."""
        pass

    def stem(self, x):
        """Stem one word by returning constant."""
        return "***"


def test_stem_method():
    """Check the _stem method."""
    tokenizer = Tokenizer("test_data/stopwords.txt", None)

    # test with no stemmer
    tokens = ["foo", "bar", "me", "your", "6502"]
    tokenizer._stem(tokens)
    assert tokens == ["foo", "bar", "me", "your", "6502"]

    # test with custom stemmer
    tokenizer = Tokenizer("test_data/stopwords.txt", stemmer=CustomStemmer())
    tokens = ["foo", "bar", "me", "your", "6502"]
    tokenizer._stem(tokens)
    assert tokens == ["foo", "bar", "me", "your", "6502"]

    # test with custom stemmer
    tokenizer = Tokenizer("test_data/stopwords.txt", stemmer=CustomStemmer2())
    tokens = ["foo", "bar", "me", "your", "6502"]
    tokenizer._stem(tokens)
    assert tokens == ["*foo", "*bar", "*me", "*your", "*6502"]

    # test with custom stemmer
    tokenizer = Tokenizer("test_data/stopwords.txt", stemmer=CustomStemmer3())
    tokens = ["foo", "bar", "me", "your", "6502"]
    tokenizer._stem(tokens)
    assert tokens == ["***", "***", "***", "***", "***"]


def sent_tokenize_mock(content):
    """Mock the function nlth.sent_tokenize."""
    return content.split(".")


def word_tokenize_mock(sentence):
    """Mock the function nlth.word_tokenize."""
    return sentence.split(" ")


@patch('nltk.sent_tokenize', side_effect=sent_tokenize_mock)
@patch('nltk.word_tokenize', side_effect=word_tokenize_mock)
def test_tokenize(mock1, mock2):
    """Check the tokenize method."""
    tokenizer = Tokenizer("test_data/stopwords.txt", 2)
    content = "The prerequisite for tagging is to collect keywords that are used " + \
              "out there by developers.This also means that tagger uses keywords " + \
              "that are considered as interesting ones by developers."
    results = tokenizer.tokenize(content)
    assert results


def sent_tokenize_mock_2(content):
    """Mock the function nlth.sent_tokenize."""
    raise LookupError("foo bar")


@patch('nltk.sent_tokenize', side_effect=sent_tokenize_mock_2)
def test_tokenize_error_handling(mock):
    """Check the tokenize method."""
    tokenizer = Tokenizer("test_data/stopwords.txt", 2)
    content = "The prerequisite for tagging is to collect keywords that are used " + \
              "out there by developers.This also means that tagger uses keywords " + \
              "that are considered as interesting ones by developers."
    with pytest.raises(InstallPrepareError) as e:
        tokenizer.tokenize(content)


if __name__ == '__main__':
    test_initial_state()
    test_stopwords_reading()
    test_raw_stopwords_property()
    test_regexp_stopwords_property()
    test_remove_stopwords_method()
    test_lemmatize_method()
    test_stem_method()
    test_tokenize()
    test_tokenize_error_handling()
