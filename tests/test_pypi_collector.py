"""Tests for the PypiCollector class."""

import pytest
from unittest.mock import *
import requests

from f8a_tagger.collectors.pypi import *


def test_initial_state():
    """Check the initial state of the class."""
    c = PypiCollector()
    assert c is not None


class _response:

    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


original_requests_get = requests.get


def mocked_requests_get(url):
    """Implement mocked function requests.get()."""
    if url == PypiCollector._PYPI_SIMPLE_URL:
        return _response(200, """
            <html>
            <head><title>Simple Index</title><meta name="api-version" value="2" /></head><body>
            <a href='mock'>mock</a><br/>
            <a href='clojure-py'>clojure_py</a><br/>
            <a href='behave'>behave</a><br/>
            <a href='0.0.1'>0.0.1</a><br/>
            <a href='selinon'>selinon</a><br/>
            </body></html>""")
    else:
        return original_requests_get(url)


# don't run this test! it take forever to finish ;)
def ___test_original_execute_method():
    """Test the execute() method."""
    c = PypiCollector()

    keywords = c.execute()


@patch("f8a_tagger.collectors.pypi.requests.get", side_effect=mocked_requests_get)
def test_execute_method(mocked_requests_get_obj):
    """Test the execute() method."""
    c = PypiCollector()

    keywords = c.execute()


def mocked_requests_get_2(url):
    """Implement mocked function requests.get()."""
    return _response(404, "Not Found")


@patch("f8a_tagger.collectors.pypi.requests.get", side_effect=mocked_requests_get_2)
def test_execute_method_negative(mocked_requests_get_obj):
    """Test the execute() method."""
    c = PypiCollector()

    with pytest.raises(RuntimeError) as e:
        keywords = c.execute()


def mocked_requests_get_3(url):
    """Implement mocked function requests.get()."""
    if url == PypiCollector._PYPI_SIMPLE_URL:
        return _response(200, """
            <html>
            <head><title>Simple Index</title><meta name="api-version" value="2" /></head><body>
            <a href='mock'>mock</a><br/>
            <a href='clojure-py'>clojure_py</a><br/>
            <a href='behave'>behave</a><br/>
            </body></html>""")
    else:
        return _response(404, "Not Found")


@patch("f8a_tagger.collectors.pypi.requests.get", side_effect=mocked_requests_get_3)
def test_execute_method_negative2(mocked_requests_get_obj):
    """Test the execute() method."""
    c = PypiCollector()

    with pytest.raises(RuntimeError) as e:
        keywords = c.execute(ignore_errors=False)

    keywords = c.execute(ignore_errors=True)


if __name__ == '__main__':
    test_initial_state()
    test_execute_method()
    test_execute_method_negative()
    test_execute_method_negative2()
