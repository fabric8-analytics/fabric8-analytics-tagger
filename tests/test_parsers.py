"""Tests for all currently supported parser classes."""

import pytest
from f8a_tagger.parsers.parsers import *


def test_initial_states():
    """Check the initial state of all parsers."""
    p = TextParser()
    assert p is not None

    p = MarkdownParser()
    assert p is not None

    p = HtmlParser()
    assert p is not None

    p = ReStructuredTextParser()
    assert p is not None

    p = AsciidocParser()
    assert p is not None

    p = TextileParser()
    assert p is not None

    p = RdocParser()
    assert p is not None

    p = OrgParser()
    assert p is not None

    p = CreoleParser()
    assert p is not None

    p = MediawikiParser()
    assert p is not None

    p = PodParser()
    assert p is not None


def test_text_parser():
    """Test the TextParser parser."""
    p = TextParser()

    parsed = p.parse("plain text content")
    assert parsed == "plain text content"


def test_markdown_parser():
    """Test the MarkdownParser parser."""
    p = MarkdownParser()

    parsed = p.parse("markdown content")
    assert parsed.strip() == "markdown content"


def test_html_parser():
    """Test the HtmlParser parser."""
    p = HtmlParser()

    parsed = p.parse("<html><body>HTML content</body></html>")
    assert parsed == "HTML content"

    parsed = p.parse("<div>two</div> <div>divs</div>")
    assert parsed == "two divs"


def test_restructuredtext_parser():
    """Test the ReStructuredTextParser parser."""
    p = ReStructuredTextParser()

    parsed = p.parse("content")
    assert parsed.strip() == "content"


def test_asciidoc_parser():
    """Test the AsciidocParser parser."""
    p = AsciidocParser()

    # this parser is not fully implemented yet
    with pytest.raises(NotImplementedError):
        p.parse("content")


def test_textile_parser():
    """Test the TextileParser parser."""
    p = TextileParser()

    # this parser is not fully implemented yet
    with pytest.raises(NotImplementedError):
        p.parse("content")


def test_rdoc_parser():
    """Test the RdocParser parser."""
    p = RdocParser()

    # this parser is not fully implemented yet
    with pytest.raises(NotImplementedError):
        p.parse("content")


def test_org_parser():
    """Test the OrgParser parser."""
    p = OrgParser()

    # this parser is not fully implemented yet
    with pytest.raises(NotImplementedError):
        p.parse("content")


def test_creole_parser():
    """Test the CreoleParser parser."""
    p = CreoleParser()

    # this parser is not fully implemented yet
    with pytest.raises(NotImplementedError):
        p.parse("content")


def test_mediawiki_parser():
    """Test the MediawikiParserparser."""
    p = MediawikiParser()

    # this parser is not fully implemented yet
    with pytest.raises(NotImplementedError):
        p.parse("content")


def test_pod_parser():
    """Test the PodParser parser."""
    p = PodParser()

    # this parser is not fully implemented yet
    with pytest.raises(NotImplementedError):
        p.parse("content")


if __name__ == '__main__':
    test_initial_states()
    test_text_parser()
    test_markdown_parser()
    test_html_parser()
    test_restructuredtext_parser()
    test_asciidoc_parser()
    test_textile_parser()
    test_rdoc_parser()
    test_org_parser()
    test_creole_parser()
    test_mediawiki_parser()
    test_pod_parser()
