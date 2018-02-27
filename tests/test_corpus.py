"""Tests for the Corpus class."""

import pytest
from f8a_tagger.corpus import Corpus


def test_initial_state():
    """Check the initial state of Corpus."""
    c = Corpus()
