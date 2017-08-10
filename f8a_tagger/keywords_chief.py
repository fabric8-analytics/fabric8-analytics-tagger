#!/usr/bin/env python3
"""Keywords loading and handling for fabric8-analytics."""

import io
import os
import re

import anymarkup
import daiquiri
import f8a_tagger.defaults as defaults
from f8a_tagger.errors import InvalidInputError

_logger = daiquiri.getLogger(__name__)


class KeywordsChief(object):
    """Keeping and interacting with keywords."""

    _DEFAULT_KEYWORD_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'keywords.yaml')

    def __init__(self, keyword_file=None, lemmatizer=False, stemmer=None):
        """Construct.

        :param keyword_file: a path to keyword file
        :param lemmatizer: lematizer instance to be used
        :param stemmer: stemmer instance to be used
        """
        self._stemmer = stemmer or defaults.DEFAULT_STEMMER
        self._lemmatizer = lemmatizer or defaults.DEFALUT_LEMMATIZER

        if isinstance(keyword_file, str) or keyword_file is None:
            with open(keyword_file or self._DEFAULT_KEYWORD_FILE_PATH, 'r') as f:
                content = f.read()
        elif isinstance(keyword_file, io.TextIOBase):
            content = keyword_file.read()
        else:
            raise InvalidInputError("Unknown keyword file provided - %s" % (type(keyword_file)))

        self._keywords = anymarkup.parse(content)
        del content

        # make sure keywords are strings
        self._keywords = dict((str(keyword), val) for keyword, val in self._keywords.items())

        # add missing default values
        for keyword in self._keywords.keys():
            if self._keywords[keyword] is None:
                self._keywords[keyword] = {'synonyms': [], 'regexp': []}

            if self._keywords[keyword].get('synonyms') is None:
                self._keywords[keyword]['synonyms'] = []

            # make sure synonyms are strings
            self._keywords[keyword]['synonyms'] = list(map(lambda x: str(x), self._keywords[keyword]['synonyms']))

            if self._keywords[keyword].get('regexp') is None:
                self._keywords[keyword]['regexp'] = []

        for keyword, entry in self._keywords.items():
            for idx, regexp in enumerate(entry['regexp']):
                entry['regexp'][idx] = re.compile(regexp)

            entry['synonyms'].append(keyword)

            for idx, synonym in enumerate(entry['synonyms']):
                for delim in [' ', '_', '-']:
                    synonyms = synonym.split(delim)
                    if self._lemmatizer:
                        synonyms = [self._lemmatizer.lemmatize(t) for t in synonyms]
                    if self._stemmer:
                        synonyms = [self._stemmer.stem(t) for t in synonyms]
                    new_synonym = delim.join(synonyms)

                    if new_synonym != synonym:
                        _logger.debug("Stemmed and lemmatized keyword synonym from '%s' to '%s' for keyword '%s'",
                                      synonym, new_synonym, keyword)
                        entry['synonyms'][idx] = new_synonym

    @property
    def keywords(self):
        """Keywords used by keywords chief instance."""
        ret = {}

        for keyword in self._keywords.keys():
            for conf in self._keywords[keyword].keys():
                if not self._keywords[keyword][conf]:
                    continue

                if keyword not in ret:
                    ret[keyword] = {}

                if conf == 'regexp':
                    ret[keyword]['regexp'] = []
                    for regexp in self._keywords[keyword]['regexp']:
                        ret[keyword]['regexp'].append(regexp.pattern)
                else:
                    ret[keyword][conf] = self._keywords[keyword][conf]

        return ret

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

        for delim in defaults.MULTIWORD_DELIMITERS:
            words = str(keyword).split(delim)
            for other_delim in defaults.MULTIWORD_DELIMITERS:
                synonyms.add(other_delim.join(words))

        return list(synonyms)

    def is_keyword(self, word):
        """Check whether the given word is a keyword.

        :param word: keyword to be checked
        :return: True if the given word is a keyword
        """
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
