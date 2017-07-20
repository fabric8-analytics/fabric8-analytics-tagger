#!/usr/bin/env python3
"""Keywords extraction/tagging for fabric8-analytics."""

import logging
import sys

import click

# Do not confuse pylint with naming
# pylint: disable=import-self,no-name-in-module
import daiquiri
from f8a_tagger.keywords_chief import KeywordsChief
from f8a_tagger.parsers import CoreParser
from f8a_tagger.tokenizer import Tokenizer
from f8a_tagger.utils import iter_files
from f8a_tagger.utils import json_dumps
import progressbar

_logger = daiquiri.getLogger(__name__)


@click.group()
@click.option('-v', '--verbose', count=True)
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
              help='Path to keywords file')
@click.option('--raw-stopwords-file', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to raw stopwords file')
@click.option('--regexp-stopwords-file', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to regexp stopwords file')
@click.option('--ignore-errors', is_flag=True,
              help='Ignore errors, but report them')
@click.option('--ngram-size', default=1, help='Ngram size')
def lookup(path, keywords_file=None, raw_stopwords_file=None, regexp_stopwords_file=None,
           ignore_errors=False, ngram_size=1):
    # pylint: disable=too-many-arguments
    """Perform keywords lookup."""
    ret = {}

    progress = progressbar.ProgressBar(widgets=[
        progressbar.Timer(), ', ',
        progressbar.Percentage(), ', ',
        progressbar.SimpleProgress(), ', ',
        progressbar.ETA()
    ])

    chief = KeywordsChief(keywords_file)
    if chief.compute_ngram_size() > ngram_size:
        _logger.warning("Computed ngram size (%d) does not reflect supplied ngram size (%d), "
                        "some synonyms will be omitted", chief.compute_ngram_size(), ngram_size)

    for file in progress(list(iter_files(path, ignore_errors))):
        _logger.info("Processing file '%s'", file)
        try:
            content = CoreParser().parse_file(file)
            tokens = Tokenizer(raw_stopwords_file, regexp_stopwords_file, ngram_size).tokenize(content)
            keywords = chief.extract_keywords(tokens)
        except Exception as exc:  # pylint: disable=broad-except
            if not ignore_errors:
                raise
            _logger.exception("Failed to parse content in file '%s': %s", file, str(exc))
            continue

        ret[file] = keywords

    print(json_dumps(ret))


if __name__ == '__main__':
    sys.exit(cli())
