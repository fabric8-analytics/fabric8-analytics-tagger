#!/usr/bin/env python3
"""Keywords scoring computation."""

import abc
import math

import daiquiri

_logger = daiquiri.getLogger(__name__)


class Scoring(metaclass=abc.ABCMeta):
    """Keywords scoring base class."""

    _scorers = {}

    @classmethod
    def register_scoring(cls, scoring_name, scorer, params=None):
        """Register scoring class.

        :param scoring_name: name of scoring
        :param scorer: scorer class
        :param params: parameters supplied to scorer's constructor
        """
        cls._scorers[scoring_name] = (scorer, params or {})

    @classmethod
    def get_registered_scorers(cls):
        """Get all registered scorers.

        :return: name of registered scorers
        """
        return list(cls._scorers.keys())

    @classmethod
    def get_scoring(cls, scoring_name, params=None):
        """Get scoring instance.

        :param scoring_name: name of scoring
        :param params: force new parameters to scorer's constructor
        :return: scorer's instance
        """
        scorer, default_params = cls._scorers[scoring_name]
        if params is None:
            params = default_params
        return scorer(**params)

    @abc.abstractmethod
    def score(self, chief, keywords):
        """Compute keywords score.

        :param chief: keywords chief instance
        :param keywords: keywords computed on lookup
        :return: keywords with computed score
        """


class CountScoring(Scoring):
    """Count scoring."""

    def score(self, chief, keywords):
        """Compute keywords score.

        :param chief: keywords chief instance
        :param keywords: keywords computed on lookup
        :return: keywords with computed score
        """
        return keywords


class RelativeUsageScoring(Scoring):
    """Relative usage scoring."""

    @staticmethod
    def _scoring_func(total_keyword_occurrence_count, keyword_occurrence_count,
                      keywords_avg_occurrence_count, total_average_occurrence_count):
        """Scoring function for relative usage.

        :param total_keyword_occurrence_count: total keyword occurrence count
        based on keywords.yaml config file
        :param keyword_occurrence_count: keyword occurrence count in the given document
        :param keywords_avg_occurrence_count: average occurrence count of found keywords
        :param total_average_occurrence_count: total average of occurrence
        count based on keywords.yaml
        :return: computed score
        """
        # pylint: disable=invalid-name
        x = ((keyword_occurrence_count + total_keyword_occurrence_count) /
             keywords_avg_occurrence_count)\
            - total_average_occurrence_count
        try:
            res = 1 / (1 + math.exp(-x))
        except OverflowError:
            if x > 0:
                return 1.0
            return 0.0
        _logger.debug("sigmoid(%g) = %g", -x, res)
        return res

    def score(self, chief, keywords):
        """Compute keywords score.

        :param chief: keywords chief instance
        :param keywords: keywords computed on lookup
        :return: keywords with computed score
        """
        ret = {}
        total_average_occurrence_count = chief.get_average_occurrence_count()
        keywords_avg_occurrence_count = sum([val / chief.keywords[keyword]['occurrence_count']
                                             for keyword, val in keywords.items()])

        for keyword, occurrence_count in keywords.items():
            _logger.debug("Scoring keyword '%s'", keyword)
            ret[keyword] = self._scoring_func(
                chief.keywords[keyword]['occurrence_count'],
                occurrence_count,
                keywords_avg_occurrence_count,
                total_average_occurrence_count)
        return ret


class TfIdfScoring(Scoring):
    """Scoring based on TF-IDF."""

    def score(self, chief, keywords):
        """Compute keywords score.

        :param chief: keywords chief instance
        :param keywords: keywords computed on lookup
        :return: keywords with computed score
        """
        raise NotImplementedError()


Scoring.register_scoring('Count', CountScoring)
Scoring.register_scoring('RelativeUsage', RelativeUsageScoring)
Scoring.register_scoring('TfIdf', TfIdfScoring)
