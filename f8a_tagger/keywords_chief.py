#!/usr/bin/env python3
"""Keywords loading and handling for fabric8-analytics."""

import os
import re

import anymarkup
import daiquiri

_logger = daiquiri.getLogger(__name__)


class KeywordsChief(object):
    """Keeping and interacting with keywords."""

    _DEFAULT_KEYWORD_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'keywords.yaml')

    def __init__(self, keyword_file_path=None):
        """Construct.

        :param keyword_file_path: a path to keyword file
        """
        with open(keyword_file_path or self._DEFAULT_KEYWORD_FILE_PATH, 'r') as f:
            self._keywords = anymarkup.parse(f.read())

        for entry in self._keywords.values():
            if entry and entry.get('regexp'):
                for idx, regexp in enumerate(entry['regexp']):
                    entry['regexp'][idx] = re.compile(regexp)

    def compute_ngram_size(self):
        """Compute ngram size based on keywords configuration.

        :return: computed ngram size
        :rtype: int
        """
        ngram_size = 1

        for entry in self._keywords.values():
            if entry and entry.get('synonyms'):
                for synonym in entry['synonyms']:
                    ngram_size = max(len(str(synonym).split(' ')), ngram_size)

        return ngram_size

    def is_keyword(self, token):
        """Check if the given token is a keyword.

        :param token: token to be checked
        :type token: str
        :return: True if the given token is a keyword
        :rtype: bool
        """
        return self._keywords.get(token) is not None

    def get_synonyms(self, keyword):
        """Get all synonyms to the given keyword.

        :param keyword: keyword to check synonyms against.
        :type keyword: str
        :return: a list of synonyms
        :rtype: list
        """
        entry = self._keywords.get(keyword)
        return entry.get('synonyms', []) if entry else []

    def get_keyword(self, token):
        """Get keyword for a token.

        :param token: token for which keyword should be found.
        :type token: str
        :return: keyword for the given token or None if no keyword was found
        """
        if token in self._keywords.keys():
            _logger.debug("Found direct keyword '%s'", token)
            return token

        for keyword, entry in self._keywords.items():
            if not entry:
                continue

            if token in (entry.get('synonyms') or []):  # pylint: disable=superfluous-parens
                _logger.debug("Found keyword '%s' based on synonym '%s'", keyword, token)
                return keyword

            for regexp in (entry.get('regexp') or []):  # pylint: disable=superfluous-parens
                if re.fullmatch(regexp, token):
                    _logger.debug("Found keyword '%s' based regexp match '%s' for '%s'", keyword, regexp.pattern, token)
                    return keyword

        return None

    def extract_keywords(self, tokens):
        """Extract all keywords.

        :param tokens: tokens for which keywords should be gathered.
        :return: a list of keywords that were found
        :rtype: list
        """
        keywords = set()

        for token in tokens:
            keyword = self.get_keyword(token)
            if keyword:
                keywords.add(keyword)

        return list(keywords)
