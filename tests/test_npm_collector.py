"""Tests for the NpmCollector class."""

import pytest
from f8a_tagger.collectors.npm import NpmCollector


def test_initial_state():
    """Check the initial state of the class."""
    c = NpmCollector()
    assert c is not None


def test_execute_method():
    """Test the execute() method."""
    c = NpmCollector()

    # this collector is not fully implemented yet
    with pytest.raises(NotImplementedError) as e:
        c.execute()


if __name__ == '__main__':
    test_initial_state()
