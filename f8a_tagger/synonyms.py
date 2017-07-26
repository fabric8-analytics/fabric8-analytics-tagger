#!/usr/bin/env python3
"""Synonyms manipulation for the given keyword."""


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
