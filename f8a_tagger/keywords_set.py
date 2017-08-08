#!/usr/bin/env python3
"""Keywords set handling for collectors."""


class KeywordsSet(object):
    """Manage keywords set for collectors."""

    def __init__(self):
        """Initialize keywords set."""
        self._keywords_set = {}

    @property
    def keywords(self):
        """Get stored keywords."""
        return self._keywords_set

    def add(self, keyword):
        """Add a keyword to set (count additions)."""
        if keyword not in self._keywords_set:
            self._keywords_set[keyword] = {}
        self._keywords_set[keyword]['occurrence_count'] = self._keywords_set[keyword].get('occurrence_count', 0) + 1

    def union(self, other):
        """Perform union on two keywords set.

        :param other: second keywords set for which union should be done
        :return: self
        :rtype: f8a_tagger.keywords_set.KeywordsSet
        """
        for keyword in other.keywords.keys():
            if keyword in self._keywords_set.keys():
                self._keywords_set[keyword]['occurrence_count'] = self._keywords_set[keyword].get('occurrence_count', 1)
            else:
                self._keywords_set[keyword] = other.keywords[keyword]

        return self
