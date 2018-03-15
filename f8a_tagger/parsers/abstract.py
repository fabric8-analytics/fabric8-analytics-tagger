#!/usr/bin/env python3
"""Abstract markup parser for fabric8-analytics."""

import abc


class AbstractParser(metaclass=abc.ABCMeta):  # pylint: disable=too-few-public-methods
    """Abstract markup parser for fabric8-analytics."""

    @abc.abstractmethod
    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
