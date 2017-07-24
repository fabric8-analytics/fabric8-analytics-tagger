#!/usr/bin/env python3
"""PyPI keywords collector."""

import requests

from bs4 import BeautifulSoup
import daiquiri
from f8a_tagger.utils import progressbarize

from .base import CollectorBase

_logger = daiquiri.getLogger(__name__)


class PypiCollector(CollectorBase):
    """PyPI keywords collector."""

    _PYPI_SIMPLE_URL = 'https://pypi.python.org/simple/'
    _PACKAGE_BASE_URL = 'https://pypi.python.org/pypi/'

    def execute(self, ignore_errors=True, use_progressbar=False):
        """Collect PyPI keywords."""
        keywords = set()

        _logger.debug("Fetching PyPI")
        response = requests.get(self._PYPI_SIMPLE_URL)
        if response.status_code != 200:
            raise RuntimeError("Failed to fetch '%s', request ended with status code %s"
                               % (self._PYPI_SIMPLE_URL, response.status_code))

        soup = BeautifulSoup(response.text, 'lxml')
        for link in progressbarize(soup.find_all('a'), use_progressbar):
            package_name = link.text
            response = requests.get("{}/{}".format(self._PACKAGE_BASE_URL, package_name))
            if response.status_code != 200:
                error_msg = "Failed to retrieve package information for '{}', response status code: {}".\
                    format(package_name, response.status_code)
                if ignore_errors:
                    _logger.error(error_msg)
                    continue
                raise RuntimeError(error_msg)

            package_soup = BeautifulSoup(response.text, 'lxml')
            meta_keywords = package_soup.find_all('meta', attrs={'name': 'keywords'})
            if len(meta_keywords) != 1:
                warn_msg = "Failed to parse and find keywords for '%s'" % package_name
                _logger.warning(warn_msg)
                continue

            # some packages have comma hardcoded in the keywords list, split keywords there as well
            found_keywords = []
            for word in meta_keywords[0].get('content', '').split(' '):
                found_keywords += [k.lower() for k in word.split(',')]

            _logger.debug("Found keywords %s in '%s'", found_keywords, package_name)
            if found_keywords:
                keywords = keywords.union(set(found_keywords))

        return list(keywords)


CollectorBase.register_collector('PyPI', PypiCollector)
