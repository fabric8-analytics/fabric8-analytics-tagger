"""Tests for the Stemmer class and for all currently supported stemmers."""

import pytest
from f8a_tagger.stemmer import Stemmer, StemmerNotFoundError

import nltk


def test_get_stemmer_positive():
    """Test for the method get_stemmer()."""
    stemmer = Stemmer.get_stemmer("LancasterStemmer")
    assert isinstance(stemmer, nltk.stem.LancasterStemmer)

    stemmer = Stemmer.get_stemmer("PorterStemmer")
    assert isinstance(stemmer, nltk.stem.PorterStemmer)

    stemmer = Stemmer.get_stemmer("EnglishStemmer")
    assert isinstance(stemmer, nltk.stem.snowball.EnglishStemmer)


def test_get_stemmer_negative():
    """Test for the method get_stemmer()."""
    with pytest.raises(StemmerNotFoundError):
        stemmer = Stemmer.get_stemmer("unknown")
        print(stemmer)

    with pytest.raises(StemmerNotFoundError):
        stemmer = Stemmer.get_stemmer("")
        print(stemmer)

    with pytest.raises(StemmerNotFoundError):
        stemmer = Stemmer.get_stemmer(None)
        print(stemmer)


def test_get_registered_stemmers():
    """Test for the class method get_registered_stemmers()."""
    stemmers = Stemmer.get_registered_stemmers()
    assert stemmers
    # we expected at least three stemmers to be registered
    assert len(stemmers) >= 3


if __name__ == '__main__':
    test_get_stemmer_positive()
    test_get_stemmer_negative()
    test_get_registered_stemmers()
