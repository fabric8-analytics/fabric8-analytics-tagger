#!/usr/bin/env python3
"""Corpus representation for fabric8-analytics."""

import json
import pickle  # Ignore B403
from sys import getsizeof

import daiquiri

_logger = daiquiri.getLogger(__name__)


class Corpus(object):
    """Corpus representation."""

    def __init__(self):
        """Construct."""
        self._entries = []
        self._names = []

    def get_memory_usage(self):
        """Get memory utilization of the corpus.

        :return: memory utilization in bytes
        :rtype: int
        """
        size = 0

        for entry in self._entries:
            size += getsizeof(entry)

        return size

    def get_size(self):
        """Get number of entries in the corpus.

        :return: total number of entries in the corpus
        :rtype: int
        """
        return len(self._entries)

    def add(self, name, entry):
        """Add entry to corpus.

        :param name: name of the file to which extracted tokens correspond
        :type name: str
        :param entry: a list of extracted tokens
        :type entry: list
        """
        self._entries.append(entry)
        self._names.append(name)

    def dump_pickle(self, path):
        """Dump whole corpus to a file using pickle.

        :param path: path to file to which dump should be done
        """
        _logger.debug("Pickling corpus to '%s'", path)
        with open(path, 'wb') as f:
            pickle.dump({'entries': self._entries, 'names': self._names}, f)
        _logger.debug("Corpus written to '%s'", path)

    def dump_json(self, path):
        """Dump whole corpus to a file, use JSON for serialization.

        :param path: path to file to which dump should be dump
        """
        _logger.debug("JSONifying corpus to '%s'", path)
        with open(path, 'w') as f:
            json.dump({'entries': self._entries, 'names': self._names}, f,
                      sort_keys=True, separators=(',', ': '), indent=2)
        _logger.debug("Corpus written to '%s'", path)

    @classmethod
    def load_pickle(cls, path):
        """Load pickle corpus dump.

        :param path: path to file from which corpus should be loaded
        """
        _logger.debug("Loading pickled corpus from '%s'", path)
        with open(path, 'rb') as f:
            content = pickle.load(f)  # Ignore B301

        instance = cls()
        instance._entries = content['entries']  # pylint: disable=protected-access
        instance._names = content['names']  # pylint: disable=protected-access
        _logger.debug("Pickled corpus loaded from '%s'", path)

        return instance

    @classmethod
    def load_json(cls, path):
        """Load JSON corpus dump.

        :param path: path to file from which corpus should be loaded
        """
        _logger.debug("Loading JSON corpus from '%s'", path)
        with open(path, 'r') as f:
            content = json.load(f)

        instance = cls()
        instance._entries = content['entries']  # pylint: disable=protected-access
        instance._names = content['names']  # pylint: disable=protected-access
        _logger.debug("JSON corpus loaded from '%s'", path)

        return instance
