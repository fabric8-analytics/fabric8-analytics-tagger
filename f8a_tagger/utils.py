#!/usr/bin/env python3
"""Utilities for fabric8-analytics tagger."""

from collections import deque
import json
import os

import daiquiri
import progressbar

_logger = daiquiri.getLogger(__name__)


def iter_files(path, ignore_errors=True):
    """Yield each file in a directory tree.

    :param path: path to a directory tree to yield files
    :param ignore_errors: do not raise exceptions but rather report them
    :return: file
    """
    stack = deque([path])

    while stack:
        item = stack.pop()

        if os.path.isfile(item):
            yield item
        elif os.path.isdir(item):
            for entry in os.listdir(item):
                stack.append(os.path.join(item, entry))
        else:
            if not ignore_errors:
                raise ValueError("Not a directory nor file '%s'" % item)

            _logger.warning("Ignoring content in '%s'", item)


def json_dumps(dictionary, pretty=True):
    """Dump dictionary to JSON, do it pretty by default.

    :param dictionary: dictionary to serialize
    :param pretty: do pretty formatting
    :return: serialized dictionary to JSON string
    """
    pretty_json_kwargs = {}
    if pretty:
        pretty_json_kwargs = {
            'sort_keys': True,
            'separators': (',', ': '),
            'indent': 2
        }

    return json.dumps(dictionary, **pretty_json_kwargs)


def progressbarize(iterable, progress=False):
    """Construct progressbar for loops if progressbar requested, otherwise return directly iterable.

    :param iterable: iterable to use
    :param progress: True if print progressbar
    """
    if progress:
        return progressbar.ProgressBar(widgets=[
            progressbar.Timer(), ', ',
            progressbar.Percentage(), ', ',
            progressbar.SimpleProgress(), ', ',
            progressbar.ETA()
        ])(list(iterable))

    return iterable
