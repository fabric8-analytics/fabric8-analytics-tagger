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
    _DEFAULT_BLACKLIST_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'blacklist.txt')

    def __init__(self, keyword_file_path=None, blacklist_file_path=None):
        """Construct.

        :param keyword_file_path: a path to keyword file
        :param blacklist_file_path: a path to keyword blacklist file
        """
        with open(keyword_file_path or self._DEFAULT_KEYWORD_FILE_PATH, 'r') as f:
            self._keywords = anymarkup.parse(f.read())

        for entry in self._keywords.values():
            if entry and entry.get('regexp'):
                for idx, regexp in enumerate(entry['regexp']):
                    entry['regexp'][idx] = re.compile(regexp)

        with open(blacklist_file_path or self._DEFAULT_BLACKLIST_FILE_PATH, 'r') as f:
            content = f.read()

        self._regexp_blacklist = []
        self._raw_blacklist = []
        for word in content.split('\n'):
            if not word:
                continue

            if word.startswith('re: '):
                _logger.debug("Adding blacklisted keyword based on regexp '%s'", word)
                self._regexp_blacklist.append(re.compile(word[len('re: '):]))
            else:
                if word.startswith('re:'):
                    _logger.warning("Found blacklisted word '%s' that starts with 're:' but there is no space "
                                    "after :, treating as raw blacklist word", word)
                _logger.debug("Adding raw blacklisted keyword '%s'", word)
                self._raw_blacklist.append(word)

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

    @staticmethod
    def filter_keyword(keyword):
        """Normalize the given keyword.

        :param keyword: keyword to normalize
        :type: str
        :return: normalized keyword with synonyms and regular expressions
        :rtype: tuple
        """
        keyword = str("-".join(str(keyword).split(" ")))
        synonyms = []
        regexp = []

        # Remove any unwanted trailing/starting characters
        change = True
        while change:
            while keyword.startswith('.'):
                keyword = keyword[1:]
                change = True

            while keyword.endswith('.'):
                keyword = keyword[:-1]
                change = True

            while keyword.startswith('_'):
                keyword = keyword[1:]
                change = True

            while keyword.endswith('_'):
                keyword = keyword[:-1]
                change = True

        return keyword, synonyms, regexp

    @staticmethod
    def compute_synonyms(keyword):
        """Compute synonyms for the given keyword.

        :param keyword: keyword for which synonyms should be computed
        :return: a list of synonyms
        """
        synonyms = set()

        words = str(keyword).split('-')
        if len(words) > 1:
            synonyms.add(' '.join(words))
            synonyms.add('.'.join(words))
            synonyms.add('_'.join(words))
            synonyms.add(''.join(words))

        words = str(keyword).split('.')
        if len(words) > 1:
            synonyms.add(' '.join(words))
            synonyms.add('-'.join(words))
            synonyms.add('_'.join(words))
            synonyms.add(''.join(words))

        words = str(keyword).split('_')
        if len(words) > 1:
            synonyms.add(' '.join(words))
            synonyms.add('-'.join(words))
            synonyms.add('.'.join(words))
            synonyms.add(''.join(words))

        return list(synonyms)

    def is_keyword(self, word):
        """Check whether the given word is a keyword.

        :param word: keyword to be checked
        :return: True if the given word is a keyword
        """
        if word in self._raw_blacklist:
            return False

        for regexp in self._regexp_blacklist:
            if re.fullmatch(regexp, word):
                return False

        return self._keywords.get(word) is not None

    def filter_keywords(self, keywords):
        """Filter and transcript keywords.

        :param keywords: keywords to be filtered as stated in the configuration file
        :type: dict
        :return: filtered keywords
        :rtype: dict
        """
        # TODO: implement
        return keywords
