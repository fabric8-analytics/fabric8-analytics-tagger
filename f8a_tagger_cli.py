#!/usr/bin/env python3
"""Keywords extraction/tagging for fabric8-analytics."""

import logging
import sys

import click

# pylint: disable=no-name-in-module
import daiquiri
from f8a_tagger.utils import json_dumps
from f8a_tagger import aggregate, lookup, collect, get_registered_collectors

_logger = daiquiri.getLogger(__name__)


@click.group()
@click.option('-v', '--verbose', count=True, help='Level of verbosity, can be applied multiple times.')
def cli(verbose=0):
    """Set up core CLI options.

    :param verbose: verbose limit
    """
    # hack based on num values of logging.DEBUG, logging.INFO, ...
    level = max(logging.ERROR - verbose * 10, logging.DEBUG)
    daiquiri.setup(outputs=(daiquiri.output.STDERR,), level=level)


@cli.command('lookup')
@click.argument('path', type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.option('--keywords-file', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to keywords file.')
@click.option('--raw-stopwords-file', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to raw stopwords file.')
@click.option('--regexp-stopwords-file', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to regexp stopwords file.')
@click.option('--ignore-errors', is_flag=True,
              help='Ignore errors, but report them.')
@click.option('--ngram-size', default=1, help='Ngram size - e.g. 2 for bigrams.')
def cli_lookup(path, **kwargs):
    """Perform keywords lookup."""
    ret = lookup(path, use_progressbar=True, **kwargs)
    print(json_dumps(ret))


@cli.command('collect')
@click.option('-c', '--collector', type=click.Choice(get_registered_collectors()), multiple=True,
              help='Resource collector to use, if none selected all collectors will be run.')
@click.option('--ignore-errors', is_flag=True,
              help='Ignore errors, but report them.')
def cli_collect(**kwargs):
    """Collect keywords from external resources."""
    ret = collect(use_progressbar=True, **kwargs)
    print(json_dumps(ret))


@cli.command('aggregate')
@click.option('-i', '--input-keywords-file',
              help="Input keywords files to use.")
@click.option('-o', '--output-keywords-file',
              help="Output keywords file with aggregated topics.")
@click.option('--no-synonyms',
              help="Do not compute synonyms.")
def cli_aggregate(**kwargs):
    """Aggregate keywords to a single file."""
    print(kwargs)
    ret = aggregate(**kwargs)
    print(json_dumps(ret))

if __name__ == '__main__':
    sys.exit(cli())
