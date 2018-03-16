"""Tests for the StackOverflowCollector class."""

import pytest
from f8a_tagger.collectors.stackoverflow import StackOverflowCollector


def test_initial_state():
    """Check the initial state of the class."""
    c = StackOverflowCollector()
    assert c is not None


def test_execute_method():
    """Test the execute() method."""
    c = StackOverflowCollector()

    keywords = c.execute()
    assert keywords.keywords
    assert len(keywords.keywords) > 0


if __name__ == '__main__':
    test_initial_state()
    test_execute_method()
