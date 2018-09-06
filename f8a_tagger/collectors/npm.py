#!/usr/bin/env python3
"""NPM keywords collector."""

from .base import CollectorBase


class NpmCollector(CollectorBase):
    """NPM keywords collector."""

    def execute(self, ignore_errors=True, use_progressbar=False):
        """Collect NPM keywords."""
        assert ignore_errors is not None
        assert use_progressbar is not None
        raise NotImplementedError()


CollectorBase.register_collector('NPM', NpmCollector)
