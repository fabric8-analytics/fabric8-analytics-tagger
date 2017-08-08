#!/usr/bin/env python3
"""Keywords loading and handling for fabric8-analytics."""

import nltk
from functools import partial

from f8a_tagger.errors import StemmerNotFoundError


class Stemmer(object):
    _SUPPORTED_STEMMERS = {
        'LancasterStemmer': (nltk.stem.LancasterStemmer, {}),
        'PorterStemmer': (nltk.stem.PorterStemmer, {}),
        'EnglishStemmer': (nltk.stem.snowball.EnglishStemmer, {})
    }

    @classmethod
    def get_stemmer(cls, stemmer_name):
        stemmer = cls._SUPPORTED_STEMMERS.get(stemmer_name)

        if stemmer is None:
            raise StemmerNotFoundError("Stemmer '%s' not found" % stemmer_name)

        return partial(stemmer[0], stemmer[1])

    @classmethod
    def get_registered_stemmers(cls):
        return list(cls._SUPPORTED_STEMMERS.keys())
