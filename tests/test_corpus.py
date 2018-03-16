"""Tests for the Corpus class."""

import pytest
from f8a_tagger.corpus import Corpus
from sys import getsizeof
import os


def test_initial_state():
    """Check the initial state of Corpus."""
    c = Corpus()
    assert c
    assert c.get_size() == 0
    assert c.get_memory_usage() == 0


def test_add_method():
    """Check the method Corpus.add()."""
    c = Corpus()
    assert c.get_size() == 0
    c.add("file1", ["token1", "token2", "token3"])
    assert c.get_size() == 1
    c.add("file2", ["token1", "token2", "token3"])
    assert c.get_size() == 2
    # name don't have to be unique
    c.add("file1", ["token1", "token2", "token3"])
    assert c.get_size() == 3


def test_get_memory_usage_method():
    """Check the method Corpus.get_memory_usage()."""
    c = Corpus()
    c.add("file1", ["test"])
    assert c.get_memory_usage() == getsizeof(["test"])
    c.add("file2", ["x", "y"])
    assert c.get_memory_usage() == getsizeof(["test"]) + getsizeof(["x", "y"])


def test_dump_pickle_method():
    """Check the method Corpus.dump_pickle()."""
    c = Corpus()
    filename = "serialized_output.dump"
    c.add("file1", ["test"])
    c.dump_pickle(filename)
    assert os.path.isfile(filename)


def test_dump_json_method():
    """Check the method Corpus.dump_json()."""
    c = Corpus()
    filename = "serialized_output.json"
    c.add("file1", ["test"])
    c.dump_json(filename)
    assert os.path.isfile(filename)


def test_load_pickle_method():
    """Check the static method Corpus.load_pickle()."""
    c = Corpus()
    filename = "serialized_output_2.dump"
    c.add("file1", ["test"])
    c.add("file2", ["foo", "bar"])
    c.dump_pickle(filename)
    c2 = Corpus.load_pickle(filename)
    assert c2.get_size() == 2
    assert "file1" in c2._names
    assert "file2" in c2._names
    assert ["test"] in c2._entries
    assert ["foo", "bar"] in c2._entries


def test_load_json_method():
    """Check the static method Corpus.load_json()."""
    c = Corpus()
    filename = "serialized_output_2.json"
    c.add("file1", ["test"])
    c.add("file2", ["foo", "bar"])
    c.dump_json(filename)
    c2 = Corpus.load_json(filename)
    assert c2.get_size() == 2
    assert "file1" in c2._names
    assert "file2" in c2._names
    assert ["test"] in c2._entries
    assert ["foo", "bar"] in c2._entries

    with pytest.raises(TypeError) as e:
        Corpus.load_json(None)


if __name__ == '__main__':
    test_initial_state()
    test_add_method()
    test_get_memory_usage_method()
    test_dump_pickle_method()
    test_dump_json_method()
    test_load_pickle_method()
    test_load_json_method()
