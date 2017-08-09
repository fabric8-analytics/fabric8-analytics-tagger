#!/usr/bin/env python3
"""Corpus representation for fabric8-analytics."""


class StemmerNotFoundError(Exception):
    """Raised if stemmer is not found."""


class InvalidInputError(Exception):
    """Raised if bad input is provided."""
