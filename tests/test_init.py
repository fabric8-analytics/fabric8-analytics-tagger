"""Tests for the __init__ script."""

import pytest
from unittest.mock import *
from f8a_tagger import *
from f8a_tagger.errors import RemoteDependencyMissingError


def test_prepare():
    """Test that the prepare() function does not fail."""
    prepare()


class _response:

    def __init__(self, status_code, text, ok):
        self.status_code = status_code
        self.text = text
        self.ok = ok


def mocked_requests_get(url):
    """Implement mocked function requests.get()."""
    assert url
    return _response(404, "Not Found", False)


@patch("requests.get", side_effect=mocked_requests_get)
def test_prepare_negative(_mocked_requests_get_obj):
    """Test the execute() method."""
    with pytest.raises(RemoteDependencyMissingError) as e:
        prepare()


if __name__ == '__main__':
    test_prepare()
    test_prepare_negative()
