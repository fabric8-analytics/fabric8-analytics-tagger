#!/usr/bin/env python3
"""NPM keywords collector."""

from .base import CollectorBase


class NpmCollector(CollectorBase):
    """NPM keywords collector."""

    def execute(self, ignore_errors=True):
        """Collect NPM keywords."""
        raise NotImplementedError()


CollectorBase.register_collector('NPM', NpmCollector)
