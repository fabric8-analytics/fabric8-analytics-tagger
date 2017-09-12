#!/usr/bin/env python3
"""Maven keywords collector."""

from json import loads
from os import path
from shutil import rmtree
from subprocess import check_output
from time import sleep

from requests import get

from bs4 import BeautifulSoup
import daiquiri
from f8a_tagger.keywords_set import KeywordsSet
from f8a_tagger.utils import cwd
from f8a_tagger.utils import get_files_dir
from f8a_tagger.utils import progressbarize

from .base import CollectorBase

_logger = daiquiri.getLogger(__name__)


class MavenCollector(CollectorBase):
    """Maven keywords collector."""

    _MVNREPOSITORY_URL = 'https://mvnrepository.com/artifact/'

    def execute(self, ignore_errors=True, use_progressbar=False):
        """Collect Maven keywords."""
        keywords_set = KeywordsSet()

        _logger.debug("Fetching Maven and executing Maven index checker")
        maven_index_checker_dir = get_files_dir()
        with cwd(maven_index_checker_dir):
            # This requires at least  4GB of free space on /tmp partition
            packages = loads(check_output(
                ['java', '-jar', path.join(maven_index_checker_dir, "maven-index-checker.jar"), '-it']))

        for package in packages:
            del package['version']
        packages = [dict(s) for s in set(frozenset(d.items()) for d in packages)]

        _logger.debug("started fetching data from mvnrepository.com")
        try:
            for package in progressbarize(packages, use_progressbar):
                package_name = package['groupId'] + '/' + package['artifactId']
                response = get(self._MVNREPOSITORY_URL + package_name)
                if response.ok is not True:
                    error_msg = "Failed to retrieve package information for '{}', response status code: {}". \
                        format(package_name, response.status_code)
                    if ignore_errors:
                        _logger.error(error_msg)
                        continue
                    raise RuntimeError(error_msg)

                soup = BeautifulSoup(response.text, 'lxml')
                for i in soup.find_all(class_="b tag"):
                    keywords_set.add(i.text)

                # It seems that mvnrepository has limit for 2000 requests per hour
                # so sleeping 2 seconds of sleep should do the trick
                sleep(2)
        finally:
            # Clean unpacked maven index after executing
            _logger.debug("Cleaning unpacked maven index")
            rmtree(path.join(maven_index_checker_dir, "target"))

        return keywords_set


CollectorBase.register_collector('Maven', MavenCollector)
