#!/usr/bin/env python3
"""Keywords loading and handling for fabric8-analytics."""

import nltk

from f8a_tagger.errors import StemmerNotFoundError


class Stemmer(object):
    """Stemmer producer."""

    _SUPPORTED_STEMMERS = {
        'LancasterStemmer': (nltk.stem.LancasterStemmer, {}),
        'PorterStemmer': (nltk.stem.PorterStemmer, {}),
        'EnglishStemmer': (nltk.stem.snowball.EnglishStemmer, {})
    }

    @classmethod
    def get_stemmer(cls, stemmer_name):
        """Get instantiated stemmer instance.

        :param stemmer_name: name of stemmer
        :return: stemmer instance
        """
        stemmer = cls._SUPPORTED_STEMMERS.get(stemmer_name)

        if stemmer is None:
            raise StemmerNotFoundError("Stemmer '%s' not found" % stemmer_name)

        return stemmer[0](**stemmer[1])

    @classmethod
    def get_registered_stemmers(cls):
        """Get listing of all registered stemmers.

        :return: a list of all registered stemmers
        """
        return list(cls._SUPPORTED_STEMMERS.keys())
