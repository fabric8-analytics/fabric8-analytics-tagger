"""Tests for functions from utils module."""

import pytest
from f8a_tagger.utils import *
from unittest.mock import *


def test_iter_files():
    """Check the iter_files iterator."""
    for i in iter_files("wrong_path"):
        assert False, "no files should be yielded"

    files = list(iter_files("test_data/"))
    assert len(files) > 0
    assert ("test_data/stopwords.txt", "test_data/stopwords.txt") in files
    assert ("test_data/directory/test_dir", "test_data/directory/test_dir") in files

    files = list(iter_files("http://google.com"))
    assert len(files) > 0

    files = list(iter_files("http://google.com/X", ignore_errors=True))
    assert not files


def test_iter_files_negative():
    """Check the iter_files iterator."""
    with pytest.raises(ValueError):
        x = list(iter_files("wrong_path", ignore_errors=False))
        assert len(x) > 0

    with pytest.raises(RuntimeError):
        x = list(iter_files("http://foobar.baz.nonexistent", ignore_errors=False))
        assert len(x) > 0

    with pytest.raises(RuntimeError):
        x = list(iter_files("http://google.com/X", ignore_errors=False))
        assert len(x) > 0


def test_json_dumps():
    """Test the function json_dumps()."""
    payload = {
        "foo": "bar",
        "X": "Y"
    }
    str = json_dumps(payload)
    assert str


def path_home_mock():
    """Mock the static method Path.home."""
    raise AttributeError()


def test_get_files_dir():
    """Test the function get_files_dir()."""
    dir = get_files_dir()
    assert dir
    assert dir.endswith(".fabric8-analytics-tagger")


# this part is relevant for Python > 3.5, but CI uses Python 3.4
# @patch('f8a_tagger.utils.Path.home', side_effect=path_home_mock)
# def test_get_files_dir_older_python(mocked_method):
#     """Test the function get_files_dir()."""
#     dir = get_files_dir()
#     assert dir
#     assert dir.endswith(".fabric8-analytics-tagger")


def test_cwd():
    """Test the generator cwd."""
    with cwd(".") as dir:
        # nothing is yielded
        assert dir is None


def test_progressbarsize():
    """Test the progressbarize function."""
    x = range(10)
    y = progressbarize(x)
    assert x == y

    z = progressbarize(x, progress=True)
    assert z


if __name__ == '__main__':
    test_iter_files()
    test_iter_files_negative()
    test_json_dumps()
    test_get_files_dir()
    test_get_files_dir_older_python()
    test_cwd()
    test_progressbarsize()
