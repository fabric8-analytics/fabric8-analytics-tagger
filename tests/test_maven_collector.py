"""Tests for the MavenCollector class."""

import pytest
from os import path, remove
from f8a_tagger.collectors.maven import MavenCollector
from f8a_tagger.errors import InstallPrepareError
from f8a_tagger.utils import get_files_dir


def test_initial_state():
    """Check the initial state of the class."""
    c = MavenCollector()
    assert c is not None


def test_execute_method():
    """Test the execute() method."""
    c = MavenCollector()

    # make sure the maven-index-checker is not present!
    filedir = get_files_dir()
    maven_index_checker_jar = path.join(filedir, "maven-index-checker.jar")
    try:
        remove(maven_index_checker_jar)
    except FileNotFoundError:
        pass

    with pytest.raises(InstallPrepareError):
        c.execute()


if __name__ == '__main__':
    test_initial_state()
    test_execute_method()
