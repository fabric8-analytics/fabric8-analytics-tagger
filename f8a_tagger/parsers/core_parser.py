#!/usr/bin/env python3
"""Main parser representation for fabric8-analytics."""


import daiquiri
import simplejson as json

from .parsers import AsciidocParser
from .parsers import CreoleParser
from .parsers import HtmlParser
from .parsers import MarkdownParser
from .parsers import MediawikiParser
from .parsers import OrgParser
from .parsers import PodParser
from .parsers import RdocParser
from .parsers import ReStructuredTextParser
from .parsers import TextileParser
from .parsers import TextParser

_logger = daiquiri.getLogger(__name__)


class CoreParser(object):
    """Main parser for fabric8-analytics."""

    _PARSERS = {
        'asciidoc': AsciidocParser,
        'creole': CreoleParser,
        'markdown': MarkdownParser,
        'mediawiki': MediawikiParser,
        'org': OrgParser,
        'pod': PodParser,
        'rdoc': RdocParser,
        'restructuredtext': ReStructuredTextParser,
        'textile': TextileParser,
        'txt': TextParser,
        'html': HtmlParser,
        # fallback to raw text when unknown format provided
        'unknown': TextParser
    }

    # based on https://github.com/github/markup#markups
    _FILE_EXTENSIONS = {
        '.adoc': 'asciidoc',
        '.asc': 'asciidoc',
        '.asciidoc': 'asciidoc',
        '.creole': 'creole',
        '.json': None,  # Checked explicitly
        '.markdown': 'markdown',
        '.md': 'markdown',
        '.mdown': 'markdown',
        '.mediawiki': 'mediawiki',
        '.mkdn': 'markdown',
        '.org': 'org',
        '.pod': 'asciidoc',
        '.rdoc': 'rdoc',
        '.rst': 'restructuredtext',
        '.textile': 'textile',
        '.txt': 'txt',
        '.wiki': 'mediawiki',
        '.html': 'html'
    }

    def parse(self, content, content_type, **parser_kwargs):
        """Parse content based on content type.

        :param content: content to be parsed.
        :param content_type: markup type to be parsed
        :param parser_kwargs: additional arguments for markup parser
        :return: parsed raw/plain content
        """
        parser_class = self._PARSERS.get(content_type.lower())

        if not parser_class:
            raise ValueError("No parser registered for content type '%s'" % content_type)

        if not content:
            raise ValueError("No content to parse")

        _logger.debug("Using parser '%s' for content type '%s'", parser_class.__name__, content_type)
        parser = parser_class(**parser_kwargs)

        return parser.parse(content)

    def parse_readme_json(self, path, **parser_kwargs):
        """Parse preprocessed README.json file.

        :param path: path to README.json file
        :type path: str
        :param parser_kwargs: additional arguments for markup parser
        :return: parsed raw/plain content
        """
        with open(path, 'r') as f:
            file_content = json.load(f)

        if not file_content:
            raise ValueError("No content in '%s'" % path)

        if 'content' not in file_content.keys():
            raise ValueError("No content in '%s', bogus README.json format?" % path)

        if 'type' not in file_content.keys():
            raise ValueError("No content type in '%s', bogus README.json format?" % path)

        return self.parse(file_content['content'], file_content['type'], **parser_kwargs)

    def parse_file(self, path, **parser_kwargs):
        """Parse file, try to determine content type.

        :param path: path to file to be parsed
        :param parser_kwargs: additional arguments for markup parser
        :return: parsed raw/plain content
        """
        if path.endswith('.json'):
            return self.parse_readme_json(path)

        for extension, content_type in self._FILE_EXTENSIONS.items():
            if path.endswith(extension):
                _logger.debug("Parsing file '%s'", path)
                with open(path, 'r') as f:
                    return self.parse(f.read(), content_type.lower(), **parser_kwargs)

        raise ValueError("Unknown file type for '%s'" % path)
