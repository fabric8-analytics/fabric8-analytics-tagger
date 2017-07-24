#!/usr/bin/env python3
"""Keywords extraction/tagging for fabric8-analytics."""

import logging
import sys

import click

# pylint: disable=no-name-in-module
import anymarkup
import daiquiri
from f8a_tagger import aggregate
from f8a_tagger import collect
from f8a_tagger import get_registered_collectors
from f8a_tagger import lookup
from f8a_tagger.utils import json_dumps

_logger = daiquiri.getLogger(__name__)


def _print_result(result, output_file):
    if not output_file or output_file == '-':
        print(json_dumps(result))
    else:
        anymarkup.serialize_file(result, output_file)


@click.group()
@click.option('-v', '--verbose', count=True, help='Level of verbosity, can be applied multiple times.')
def cli(verbose=0):
    """Set up core CLI options."""
    # hack based on num values of logging.DEBUG, logging.INFO, ...
    level = max(logging.ERROR - verbose * 10, logging.DEBUG)
    daiquiri.setup(outputs=(daiquiri.output.STDERR,), level=level)


@cli.command('lookup')
@click.argument('path', type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.option('-o', '--output-file',
              help="Output file with found keywords.")
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
    output_file = kwargs.pop('output_file')
    ret = lookup(path, use_progressbar=True, **kwargs)
    _print_result(ret, output_file)


@cli.command('collect')
@click.option('-c', '--collector', type=click.Choice(get_registered_collectors()), multiple=True,
              help='Resource collector to use, if none selected all collectors will be run.')
@click.option('-o', '--output-keywords-file',
              help="Output keywords file with keywords.")
@click.option('--ignore-errors', is_flag=True,
              help='Ignore errors, but report them.')
def cli_collect(**kwargs):
    """Collect keywords from external resources."""
    output_keywords_file = kwargs.pop('output_keywords_file')
    ret = collect(use_progressbar=True, **kwargs)
    _print_result(ret, output_keywords_file)


@cli.command('aggregate')
@click.option('-i', '--input-keywords-file', multiple=True,
              help="Input keywords files to use.")
@click.option('-o', '--output-keywords-file',
              help="Output keywords file with aggregated keywords.")
@click.option('--no-synonyms',
              help="Do not compute synonyms.")
def cli_aggregate(**kwargs):
    """Aggregate keywords to a single file."""
    output_keywords_file = kwargs.pop('output_keywords_file')
    ret = aggregate(use_progressbar=True, **kwargs)
    _print_result(ret, output_keywords_file)


if __name__ == '__main__':
    sys.exit(cli())
