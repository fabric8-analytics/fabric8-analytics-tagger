#!/usr/bin/env python3
"""Synonyms manipulation for the given keyword."""


def compute_synonyms(keyword):
    """Compute synonyms for the given keyword.

    :param keyword: keyword for which synonyms should be computed
    :return: a list of synonyms
    """
    synonyms = set()

    synonyms = synonyms.union(' '.join(keyword.split('-')))
    synonyms = synonyms.union(' '.join(keyword.split('.')))
    synonyms = synonyms.union('-'.join(keyword.split('.')))
    synonyms = synonyms.union('.'.join(keyword.split('-')))

    return list(synonyms) or None
