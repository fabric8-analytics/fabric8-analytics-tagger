#!/usr/bin/env python3
"""PyPI keywords collector."""

import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

import daiquiri
from f8a_tagger.keywords_set import KeywordsSet
from f8a_tagger.utils import progressbarize

from .base import CollectorBase

_logger = daiquiri.getLogger(__name__)


class PypiCollector(CollectorBase):
    """PyPI keywords collector."""

    _PYPI_SIMPLE_URL = 'https://pypi.python.org/simple/'
    _PACKAGE_BASE_URL = 'https://pypi.python.org/pypi/project'

    def execute(self, ignore_errors=True, use_progressbar=False):
        """Collect PyPI keywords."""
        keywords_set = KeywordsSet()

        _logger.debug("Fetching PyPI")
        response = requests.get(self._PYPI_SIMPLE_URL)
        if response.status_code != 200:
            raise RuntimeError("Failed to fetch '%s', request ended with status code %s"
                               % (self._PYPI_SIMPLE_URL, response.status_code))

        soup = BeautifulSoup(response.text, 'lxml')
        for link in progressbarize(soup.find_all('a'), use_progressbar):
            package_name = link.text
            url = urljoin(self._PACKAGE_BASE_URL, package_name)
            response = requests.get(url)
            if response.status_code != 200:
                error_msg = "Failed to retrieve package information for '{}', " \
                            "response status code: {}".\
                    format(package_name, response.status_code)
                if ignore_errors:
                    _logger.error(error_msg)
                    continue
                raise RuntimeError(error_msg)

            package_soup = BeautifulSoup(response.text, 'lxml')
            # meta_keywords = package_soup.find_all('meta', attrs={'name': 'keywords'})
            meta_keywords = package_soup.find_all('p', attrs={'class': 'tags'})
            if len(meta_keywords) < 1:
                warn_msg = "Failed to parse and find keywords for '%s'" % package_name
                _logger.warning(warn_msg)
                continue

            # some packages have comma hardcoded in the keywords list, split keywords there as well
            found_keywords = []
            keywords_spans = meta_keywords[0].find_all('span', attrs={'class': 'package-keyword'})
            for span in keywords_spans:
                for word in span.contents:
                    found_keywords += [k.strip().lower() for k in word.split(',')
                                       if k.strip() != ""]

            _logger.debug("Found keywords %s in '%s'", found_keywords, package_name)

            for keyword in set(found_keywords):
                keywords_set.add(keyword)

        return keywords_set


CollectorBase.register_collector('PyPI', PypiCollector)
