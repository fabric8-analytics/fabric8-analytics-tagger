"""Tests for the Lemmatizer class."""

import pytest
from f8a_tagger.lemmatizer import *

from nltk.stem.wordnet import WordNetLemmatizer


def test_get_lemmatizer():
    """Test for the method get_lemmatizer()."""
    lemmatizer = Lemmatizer.get_lemmatizer()
    assert isinstance(lemmatizer, WordNetLemmatizer)


if __name__ == '__main__':
    test_get_lemmatizer()
