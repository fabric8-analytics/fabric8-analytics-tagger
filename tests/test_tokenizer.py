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


if __name__ == '__main__':
    test_initial_state()
    test_stopwords_reading()
