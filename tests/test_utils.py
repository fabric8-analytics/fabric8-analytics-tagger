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
    with pytest.raises(ValueError) as e:
        x = list(iter_files("wrong_path", ignore_errors=False))
        assert len(x) > 0

    with pytest.raises(RuntimeError) as e:
        x = list(iter_files("http://foobar.baz.nonexistent", ignore_errors=False))
        assert len(x) > 0

    with pytest.raises(RuntimeError) as e:
        x = list(iter_files("http://google.com/X", ignore_errors=False))
        assert len(x) > 0
