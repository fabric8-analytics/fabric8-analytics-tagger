#!/usr/bin/env python3
"""Utilities for fabric8-analytics tagger."""

from collections import deque
from contextlib import contextmanager
import json
import os
from os import chdir
from os import getcwd
import tempfile

import requests

import daiquiri
from f8a_tagger.errors import RemoteResourceMissingError
import progressbar

_logger = daiquiri.getLogger(__name__)


def _get_remote_resource(item):
    """Get remote resource (e.g. README file).

    :param item: remote resource location
    :return: tuple - content and content extension based on content type
    """
    response = requests.get(item)
    if response.status_code != 200:
        raise RemoteResourceMissingError("Server returned HTTP status code: %d"
                                         % response.status_code)
    parts = item.rsplit('.', 1)
    if len(parts) > 2:
        return response.text, '.' + parts[-1]

    # Use HTML parser by default
    return response.text, '.html'


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
            yield item, item
        elif os.path.isdir(item):
            for entry in os.listdir(item):
                stack.append(os.path.join(item, entry))
        elif item.startswith(('http://', 'https://')):
            try:
                content, suffix = _get_remote_resource(item)
                temp_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False, suffix=suffix)
                temp_file.write(content)
                temp_file.close()
            except Exception as exc:  # pylint: disable=broad-except
                error_msg = "Failed to retrieve remote file for '%s': %s" % (item, str(exc))
                if not ignore_errors:
                    raise RuntimeError(error_msg) from exc

                _logger.warning(error_msg)
                continue
            yield item, temp_file
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
        # The casting to list is due to possibly yielded value that prevents ProgressBar to compute overall ETA
        return progressbar.ProgressBar(widgets=[
            progressbar.Timer(), ', ',
            progressbar.Percentage(), ', ',
            progressbar.SimpleProgress(), ', ',
            progressbar.ETA()
        ])(list(iterable))

    return iterable


@contextmanager
def cwd(target):
    """Manage cwd in a pushd/popd fashion."""
    curdir = getcwd()
    chdir(target)
    try:
        yield
    finally:
        chdir(curdir)
