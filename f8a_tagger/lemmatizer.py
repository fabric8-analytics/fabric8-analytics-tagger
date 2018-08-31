#!/usr/bin/env python3
"""Lemmatizer handling in fabric8-analytics-tagger."""

from nltk.stem.wordnet import WordNetLemmatizer


class Lemmatizer(object):  # pylint: disable=too-few-public-methods
    """Lemmatizer producer."""

    @classmethod
    def get_lemmatizer(cls):
        """Get lemmatizer instance."""
        assert cls is not None
        return WordNetLemmatizer()
