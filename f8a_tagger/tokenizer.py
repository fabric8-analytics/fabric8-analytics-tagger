#!/usr/bin/env python3
"""Tokenizer for fabric8-analytics tagger."""

import io
import os
import re

import nltk

import daiquiri
from f8a_tagger.errors import InvalidInputError

_logger = daiquiri.getLogger(__name__)


class Tokenizer(object):
    """Tokenizer for fabric8-analytics."""

    _STOPWORDS_TXT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'stopwords.txt')

    def __init__(self, stopwords_file=None, ngram_size=1, lemmatizer=None, stemmer=None):
        """Construct.

        :param stopwords_file: path to stopwords file or file
        :type stopwords_file: str
        :param ngram_size: size of ngrams that should be constructed from tokens
        :type ngram_size: int
        :param lemmatizer: lemmatizer instance to be used
        :param stemmer: stemmer instance to be used
        """
        self._ngram_size = ngram_size
        _logger.debug('ngram size is %d', self._ngram_size)

        self._regexp_stopwords = []
        self._raw_stopwords = []
        self._stemmer = stemmer
        self._lemmatizer = lemmatizer

        if isinstance(stopwords_file, str) or stopwords_file is None:
            with open(stopwords_file or self._STOPWORDS_TXT, 'r') as f:
                content = f.read()
        elif isinstance(stopwords_file, io.TextIOBase):
            content = stopwords_file.read()
        else:
            raise InvalidInputError("Invalid stopword file provided '%s' (type %s)"
                                    % (stopwords_file, type(stopwords_file)))

        for word in content.split('\n'):
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

        _logger.debug('Registered raw stopwords without lemmatization and stemming: %s', self._raw_stopwords)

        self._lemmatize(self._raw_stopwords, stopwords=True)
        self._stem(self._raw_stopwords, stopwords=True)

        _logger.debug('Registered raw stopwords with lemmatization and stemming: %s', self._raw_stopwords)

        _logger.debug('Registered regexp stopwords: %s',
                      [regexp.pattern for regexp in self._regexp_stopwords])

    def _lemmatize(self, tokens, stopwords=False):
        """Lemmatize a list of tokens.

        :param tokens: a list of tokens to lemmatize
        """
        if self._lemmatizer:
            for idx, token in enumerate(tokens):
                new_token = self._lemmatizer.lemmatize(token)
                if new_token != token:
                    _logger.debug("Lemmatized %s '%s' to '%s'",
                                  'stopword' if stopwords else 'token', token, new_token)
                    tokens[idx] = new_token
        else:
            _logger.debug("Lemmatization will not be performed.")

    def _stem(self, tokens, stopwords=False):
        """Perform stemming on a list of tokens.

        :param tokens: a list of tokens to stem
        """
        if self._stemmer:
            for idx, token in enumerate(tokens):
                new_token = self._stemmer.stem(token)
                if new_token != token:
                    _logger.debug("Stemmed %s '%s' to '%s'",
                                  'stopword' if stopwords else 'token', token, new_token)
                    tokens[idx] = new_token
        else:
            _logger.debug("Stemming will not be performed.")

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
        sentences = nltk.sent_tokenize(content)

        for idx, sentence in enumerate(sentences):
            sentences[idx] = [token.lower() for token in nltk.word_tokenize(sentence)]

        _logger.debug('Extracted tokens without lemmatization and stemming: %s', sentences)

        for idx, sentence in enumerate(sentences):
            self._lemmatize(sentence)
            self._stem(sentence)
        _logger.debug('Extracted tokens with lemmatization and stemming: %s', sentences)

        if remove_stopwords:
            for idx, sentence in enumerate(sentences):
                sentences[idx] = self.remove_stopwords(sentence)
            _logger.debug('Extracted tokens without stopwords: %s', sentences)

        # append computed ngrams at the end
        if self._ngram_size > 1:
            sentences.append([])

        for sentence in sentences[:-1]:
            for i in range(1, self._ngram_size):
                sentences[-1] += [" ".join(ngram) for ngram in zip(*[sentence[j:] for j in range(i + 1)])]

        _logger.debug('Final tokens with ngrams (ngram size: %d): %s', self._ngram_size, sentences)

        return sentences
