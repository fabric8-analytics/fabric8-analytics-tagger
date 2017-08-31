#!/usr/bin/env python3
"""Markup specific parsers implementation for fabric8-analytics."""

from docutils.core import publish_string

from bs4 import BeautifulSoup
import daiquiri
import markdown2

from .abstract import AbstractParser

_logger = daiquiri.getLogger(__name__)


class TextParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """Plain text parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        return content


class MarkdownParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """Markdown parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        return BeautifulSoup(markdown2.markdown(content), 'lxml').get_text()


class HtmlParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """HTML parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        return BeautifulSoup(content, 'lxml').get_text()


class ReStructuredTextParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """ReStructuredText parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        return BeautifulSoup(publish_string(content,
                                            parser_name='restructuredtext',
                                            writer_name='html'),
                             'lxml').find('body').get_text()


class AsciidocParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """ASCII doc parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        raise NotImplementedError("Parser '%s' not implemented", self.__class__.__name__)


class TextileParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """Textile parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        # TODO: implement
        raise NotImplementedError("Parser '%s' not implemented", self.__class__.__name__)


class RdocParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """RDoc parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        # TODO: implement
        raise NotImplementedError("Parser '%s' not implemented", self.__class__.__name__)


class OrgParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """Org parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        # TODO: implement
        raise NotImplementedError("Parser '%s' not implemented", self.__class__.__name__)


class CreoleParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """Creole parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        # TODO: implement
        raise NotImplementedError("Parser '%s' not implemented", self.__class__.__name__)


class MediawikiParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """MediaWiki parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        # TODO: implement
        raise NotImplementedError("Parser '%s' not implemented", self.__class__.__name__)


class PodParser(AbstractParser):  # pylint: disable=too-few-public-methods
    """Pod parser."""

    def parse(self, content):
        """Parse content to raw text.

        :param content: content to parse
        :type content: str
        :return: raw/plain content representation
        :rtype: str
        """
        # TODO: implement
        raise NotImplementedError("Parser '%s' not implemented", self.__class__.__name__)
