#!/usr/bin/env python3
"""Corpus representation for fabric8-analytics."""


class StemmerNotFoundError(Exception):
    """Raised if stemmer is not found."""


class InvalidInputError(Exception):
    """Raised if bad input is provided."""


class RemoteResourceMissingError(Exception):
    """Raised when remote resource (e.g. README) is not found."""


class RemoteDependencyMissingError(Exception):
    """Raised when remote dependency (e.g. maven-index-checker) is not found."""


class InstallPrepareError(Exception):
    """Raised when prepare() was not called after installation."""
