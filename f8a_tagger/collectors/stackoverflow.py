#!/usr/bin/env python3
"""PyPI keywords collector."""

import requests
import libarchive
import xmltodict
import daiquiri
from f8a_tagger.keywords_set import KeywordsSet
from f8a_tagger.utils import progressbarize

from .base import CollectorBase

_logger = daiquiri.getLogger(__name__)


class StackoverflowCollector(CollectorBase):
    """Stackoverflow keywords collector."""

    _STACKOVERFLOW_URL = 'https://archive.org/download/stackexchange/stackoverflow.com-Tags.7z'

    def execute(self, ignore_errors=True, use_progressbar=False):
        """Collect PyPI keywords."""

        keywords_set = KeywordsSet()
        _logger.debug("Fetching Stackoverflow")
        _STACKOVERFLOW_URL = 'https://archive.org/download/stackexchange/stackoverflow.com-Tags.7z'

        response = requests.get(_STACKOVERFLOW_URL)
        if response.ok is not True:
            raise RuntimeError("Failed to fetch '%s', request ended with status code %s"
                               % (self._STACKOVERFLOW_URL, response.status_code))

        tags = None
        # do the unpacking
        with libarchive.memory_reader(response.content) as archive:
            for entry in archive:
                if entry.name == 'Tags.xml':
                    tags = xmltodict.parse(b"".join(entry.get_blocks()))

        for tag in tags['tags']['row']:
            keywords_set.add(tag['@TagName'], int(tag['@Count']))

        return keywords_set


CollectorBase.register_collector('Stackoverflow', StackoverflowCollector)
