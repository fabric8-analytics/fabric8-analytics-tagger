#!/usr/bin/env python3
"""StackOverflow keywords collector."""

import requests

import daiquiri
from f8a_tagger.keywords_set import KeywordsSet
import libarchive
import xmltodict

from .base import CollectorBase

_logger = daiquiri.getLogger(__name__)


class StackOverflowCollector(CollectorBase):
    """StackOverflow keywords collector."""

    _STACKOVERFLOW_URL = 'https://archive.org/download/stackexchange/stackoverflow.com-Tags.7z'

    def execute(self, ignore_errors=True, use_progressbar=False):
        """Collect PyPI keywords."""
        keywords_set = KeywordsSet()
        _logger.debug("Fetching StackOverflow")

        response = requests.get(self._STACKOVERFLOW_URL)
        if response.ok is not True:
            raise RuntimeError("Failed to fetch '%s', request ended with status code %s"
                               % (self._STACKOVERFLOW_URL, response.status_code))

        tags = None
        _logger.debug("Unpacking StackOverflow's tags archive")
        with libarchive.memory_reader(response.content) as archive:
            for entry in archive:
                if entry.name == 'Tags.xml':
                    tags = xmltodict.parse(b"".join(entry.get_blocks()))
                    break

        for tag in tags['tags']['row']:
            try:
                keywords_set.add(tag['@TagName'], int(tag['@Count']))
            except ValueError:
                _logger.warning("Failed to parse number of occurrences for tag %s", tag['@TagName'])
                continue
            except KeyError:
                _logger.exception("Missing tagname or tag count")
                continue

        return keywords_set


CollectorBase.register_collector('StackOverflow', StackOverflowCollector)
