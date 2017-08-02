#!/usr/bin/env python3
"""Base class for collectors."""

import abc


class CollectorBase(metaclass=abc.ABCMeta):
    """Base class for collectors."""

    _collectors = {}

    @abc.abstractmethod
    def execute(self, ignore_errors=True, use_progressbar=False):
        """Collect keywords.

        :param ignore_errors: ignore any non-critical error
        :param use_progressbar: report progress with progressbar
        :return: keywords set
        :rtype: f8a_tagger.keywords_set.KeywordsSet
        """
        pass

    @classmethod
    def register_collector(cls, collector_name, collector):
        """Register collector to global collectors.

        :param collector_name: collector name to register
        :param collector: collector to register
        """
        if collector_name in cls._collectors.keys():
            raise ValueError("Collector '%s' already registered using class '%s'"
                             % (collector_name, collector.__name__))

        cls._collectors[collector_name] = collector

    @classmethod
    def get_registered_collectors(cls):
        """Get all registered collectors."""
        return list(cls._collectors.keys())

    @classmethod
    def get_collector_class(cls, collector_name):
        """Get collector by its name.

        :param collector_name: name of the collector to get
        """
        try:
            return cls._collectors[collector_name]
        except KeyError:
            raise KeyError("No collector with name '%s' found" % collector_name)
