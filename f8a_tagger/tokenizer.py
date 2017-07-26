#!/usr/bin/env python3
"""Tokenizer for fabric8-analytics tagger."""

import os
import re

import nltk

import daiquiri

_logger = daiquiri.getLogger(__name__)


class Tokenizer(object):
    """Tokenizer for fabric8-analytics."""

    _STOPWORDS_TXT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'stopwords.txt')

    def __init__(self, stopwords_file=None, ngram_size=1):
        """Construct.

        :param raw_stopwords: path to raw stopwords file
        :type raw_stopwords: str
        :param regexp_stopwords: path to regexp stopwords file
        :type regexp_stopwords: str
        :param ngram_size: size of ngrams that should be constructed from tokens
        :type ngram_size: int
        """
        self._ngram_size = ngram_size
        _logger.debug('ngram size is %d', self._ngram_size)

        self._regexp_stopwords = []
        self._raw_stopwords = []

        with open(stopwords_file or self._STOPWORDS_TXT, 'r') as f:
            for word in f.read().split('\n'):
                # Remove comments
                if word.startswith('#') and word != '#':
                    continue

                if word.startswith('re: '):
                    self._regexp_stopwords.append(re.compile(word[len('re: '):]))
                else:
                    if word.startswith('re:'):
                        _logger.warning("Stopword listed in '%s' starts with 're:' but treating as raw "
                                        "stopword, missing space after?")
                    self._raw_stopwords.append(word)

        _logger.debug('Registered raw stopwords: %s', self._raw_stopwords)
        _logger.debug('Registered regexp stopwords: %s', [regexp.pattern for regexp in self._regexp_stopwords])

    def remove_stopwords(self, tokens):
        """Remove stopwords from token list.

        :param tokens: tokens from which stopwords should be removed
        :type tokens: list
        :return: tokens with filtered out stopwords
        """
        ret = []

        for token in tokens:
            if token in self._raw_stopwords:
                _logger.debug("Dropping raw stopword '%s'", token)
                continue

            for regexp in self._regexp_stopwords:
                if re.fullmatch(regexp, token):
                    _logger.debug("Dropping stopword '%s' based on regexp '%s'", token, regexp.pattern)
                    continue

            ret.append(token)

        return ret

    def tokenize(self, content, remove_stopwords=True):
        """Tokenize plain content.

        :param content: content to tokenize
        :type content: str
        :param remove_stopwords: remove stopwords after tokenization
        :type remove_stopwords: bool
        :return: tokenized content
        """
        tokens = [token.lower() for token in nltk.word_tokenize(content)]
        _logger.debug('Extracted tokens (size %d): %s', len(tokens), tokens)

        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)
            _logger.debug('Extracted tokens without stopwords (size: %d): %s', len(tokens), tokens)

        for i in range(1, self._ngram_size):
            tokens += [" ".join(ngram) for ngram in zip(*[tokens[j:] for j in range(i + 1)])]

        _logger.debug('Extracted tokens with ngrams (size %d, ngram size: %d): %s',
                      len(tokens), self._ngram_size, tokens)

        return tokens
