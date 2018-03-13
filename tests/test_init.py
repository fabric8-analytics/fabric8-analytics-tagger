"""Tests for the __init__ script."""

import __init__
import pytest

def test_logger():
    """Test the logger initialized in __init__."""
    assert __init__.logger is not None


if __name__ == '__main__':
    test_logger()
