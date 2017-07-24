#!/usr/bin/env python3
"""Maven keywords collector."""

from .base import CollectorBase


class MavenCollector(CollectorBase):
    """Maven keywords collector."""

    def execute(self, ignore_errors=True, use_progressbar=False):
        """Collect Maven keywords."""
        raise NotImplementedError()


CollectorBase.register_collector('Maven', MavenCollector)
