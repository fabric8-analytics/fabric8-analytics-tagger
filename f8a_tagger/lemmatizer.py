#!/usr/bin/env python3
"""Lemmatizer handling in fabric8-analytics-tagger."""

from nltk.stem.wordnet import WordNetLemmatizer


class Lemmatizer(object):
    """Lemmatizer producer."""

    @classmethod
    def get_lemmatizer(cls):
        """Get lemmatizer instance."""
        return WordNetLemmatizer()
