"""Tests for the StackOverflowCollector class."""

import pytest
from unittest.mock import *
from f8a_tagger.collectors.stackoverflow import StackOverflowCollector
from f8a_tagger.keywords_set import KeywordsSet


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


class _response:

    def __init__(self, status_code, ok, text):
        self.status_code = status_code
        self.ok = ok
        self.text = text


def mocked_requests_1(url):
    """Implement mocked function requests.get()."""
    assert url
    return _response(200, False, """
        <html>
        <head><title>Simple Index</title><meta name="api-version" value="2" /></head><body>
        <a href='mock'>mock</a><br/>
        <a href='clojure-py'>clojure_py</a><br/>
        <a href='behave'>behave</a><br/>
        </body></html>""")


@patch("f8a_tagger.collectors.stackoverflow.requests.get", side_effect=mocked_requests_1)
def test_execute_method_negative1(_mocked_get):
    """Test the execute() method."""
    c = StackOverflowCollector()

    with pytest.raises(RuntimeError) as e:
        keywords = c.execute()


mocked_add_called = False
orig_add = KeywordsSet.add


def mocked_add(self, x, y):
    """Mock add method for KeywordsSet.add()."""
    global mocked_add_called
    if mocked_add_called:
        orig_add(self, x, y)
    else:
        mocked_add_called = True
        # throw ValueError exception
        x = int("foobar")


@patch("f8a_tagger.keywords_set.KeywordsSet.add", side_effect=mocked_add, autospec=True)
def test_execute_method_negative2(_mocked_add):
    """Test the execute() method."""
    c = StackOverflowCollector()

    keywords = c.execute()
    assert keywords.keywords
    assert len(keywords.keywords) > 0


mocked_add_2_called = False


def mocked_add_2(self, x, y):
    """Mock add method for KeywordsSet.add()."""
    global mocked_add_2_called
    if mocked_add_2_called:
        orig_add(self, x, y)
    else:
        mocked_add_2_called = True
        # throw KeyError exception
        x = {}
        y = x["foobar"]


@patch("f8a_tagger.keywords_set.KeywordsSet.add", side_effect=mocked_add_2, autospec=True)
def test_execute_method_negative3(_mocked_add):
    """Test the execute() method."""
    c = StackOverflowCollector()

    keywords = c.execute()
    assert keywords.keywords
    assert len(keywords.keywords) > 0


if __name__ == '__main__':
    test_initial_state()
    test_execute_method()
    test_execute_method_negative1()
    test_execute_method_negative2()
    test_execute_method_negative3()
