#!/usr/bin/env python3
"""Maven keywords collector."""

from json import loads
from os import chdir, path
from pathlib import Path
from subprocess import check_output

from requests import get

from bs4 import BeautifulSoup
import daiquiri
from f8a_tagger.keywords_set import KeywordsSet
from f8a_tagger.utils import progressbarize

from .base import CollectorBase

_logger = daiquiri.getLogger(__name__)


class MavenCollector(CollectorBase):
    """PyPI keywords collector."""
    _MVNREPOSITORY_URL = 'https://mvnrepository.com/artifact/'

    def execute(self, ignore_errors=True, use_progressbar=False):
        """Collect Maven keywords."""
        keywords_set = KeywordsSet()

        _logger.debug("Fetching MVN")
        _logger.debug("execute maven index checker")
        chdir('/tmp')
        # This requires at least  4GB of free space on /tmp partition
        packages = loads(check_output(
            ['java', '-jar', path.join(Path.home(), ".fabric8-analytics-tagger", "maven-index-checker.jar"), '-it']))
        for package in packages:
            del package['version']
        packages = [dict(s) for s in set(frozenset(d.items()) for d in packages)]

        _logger.debug("started fetching data from mvnrepository.com")
        for package in progressbarize(packages, True):
            response = get(self._MVNREPOSITORY_URL + package['groupId'] + '/' + package['artifactId'])
            soup = BeautifulSoup(response.text, 'lxml')
            for i in soup.find_all(class_="b tag"):
                keywords_set.add(i.text)

        return keywords_set


CollectorBase.register_collector('Maven', MavenCollector)
