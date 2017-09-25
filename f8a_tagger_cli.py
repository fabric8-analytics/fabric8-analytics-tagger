#!/usr/bin/env python3
"""Keywords extraction/tagging for fabric8-analytics."""

import logging
import operator
import sys

import click
import yaml

# pylint: disable=no-name-in-module
import anymarkup
import daiquiri
from f8a_tagger import aggregate
from f8a_tagger import collect
from f8a_tagger import get_registered_collectors
from f8a_tagger import get_registered_scorers
from f8a_tagger import get_registered_stemmers
from f8a_tagger import lookup_file
from f8a_tagger import reckon
import f8a_tagger.defaults as defaults
from f8a_tagger.utils import json_dumps

_logger = daiquiri.getLogger(__name__)


def _print_result(result, output_file, fmt=None):
    if not output_file or output_file == '-':
        if fmt == 'yaml' or fmt == 'yml':
            print(yaml.dump(result))
        elif fmt == 'json' or fmt is None:
            print(json_dumps(result))
        else:
            raise ValueError("Unknown output format '%s'" % fmt)
    else:
        if fmt is None:  # try to guess format by file extension
            extension = output_file.split('.')[-1]
            if extension in ('yaml', 'yml', 'json'):
                fmt = extension if extension != 'yml' else 'yaml'
            else:
                fmt = defaults.DEFAULT_OUTPUT_FORMAT
        _logger.debug("Serializing output to file '%s'", output_file)
        anymarkup.serialize_file(result, output_file, format=fmt)


@click.group()
@click.option('-v', '--verbose', count=True, help='Level of verbosity, can be applied multiple times.')
def cli(verbose=0):
    """Tagger for fabric8-analytics."""
    # hack based on num values of logging.DEBUG, logging.INFO, ...
    level = max(logging.WARNING - verbose * 10, logging.DEBUG)
    daiquiri.setup(outputs=(daiquiri.output.STDERR,), level=level)


@cli.command('lookup')
@click.argument('path', type=click.Path())
@click.option('-o', '--output-file',
              help='Output file with found keywords.')
@click.option('--keywords-file', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to keywords file.')
@click.option('--stopwords-file', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to stopwords file.')
@click.option('--ignore-errors', is_flag=True,
              help='Ignore errors, but report them.')
@click.option('-f', '--output-format',
              help='Output keywords format/type.')
@click.option('--stemmer', type=click.Choice(get_registered_stemmers()), multiple=False,
              help='Stemmer type to be used, default: %s.' % defaults.DEFAULT_STEMMER)
@click.option('--lemmatize', is_flag=True,
              help='Use lemmatizer, default: %s' % defaults.DEFAULT_LEMMATIZER)
@click.option('--ngram-size', default=None, type=int,
              help='Ngram size - e.g. 2 for bigrams, if not provided, '
                   'ngram size is computed based on keywords.yaml file.')
@click.option('--scorer', type=click.Choice(get_registered_scorers()), multiple=False,
              help='Keywords scoring mechanism to be used, default: %s' % defaults.DEFAULT_SCORER)
@click.option('--summary', '-s', is_flag=True,
              help='Print sorted summary.')
def cli_lookup(path, **kwargs):
    """Perform keywords lookup."""
    output_file = kwargs.pop('output_file')
    output_format = kwargs.pop('output_format')
    summary = kwargs.pop('summary')
    ret = lookup_file(path, use_progressbar=True, **kwargs)
    if summary:
        total = {}
        for f in ret:
            total[f] = sorted(ret[f].items(), key=operator.itemgetter(1), reverse=True)
        _print_result(total, output_file, output_format)
    else:
        _print_result(ret, output_file, output_format)


@cli.command('collect')
@click.option('-c', '--collector', type=click.Choice(get_registered_collectors()), multiple=True,
              help='Resource collector to use, if none selected all collectors will be run.')
@click.option('-o', '--output-keywords-file',
              help='Output keywords file with keywords.')
@click.option('-f', '--output-format',
              help='Output keywords format/type.')
@click.option('--ignore-errors', is_flag=True,
              help='Ignore errors, but report them.')
def cli_collect(**kwargs):
    """Collect keywords from external resources."""
    output_keywords_file = kwargs.pop('output_keywords_file')
    output_format = kwargs.pop('output_format')
    ret = collect(use_progressbar=True, **kwargs)
    _print_result(ret, output_keywords_file, output_format)


@cli.command('aggregate')
@click.option('-i', '--input-keywords-file', multiple=True,
              help='Input keywords files to use.')
@click.option('-o', '--output-keywords-file',
              help='Output keywords file with aggregated keywords.')
@click.option('-f', '--output-format',
              help='Output keywords file format/type.')
@click.option('--no-synonyms',
              help='Do not compute synonyms.')
@click.option('--occurrence-count-filter', type=int,
              help="Filter out synonyms with low occurrence count (default: %d)." % defaults.OCCURRENCE_COUNT_FILTER)
def cli_aggregate(**kwargs):
    """Aggregate keywords to a single file."""
    output_keywords_file = kwargs.pop('output_keywords_file')
    output_format = kwargs.pop('output_format')
    if kwargs['occurrence_count_filter'] is None:
        kwargs['occurrence_count_filter'] = defaults.OCCURRENCE_COUNT_FILTER
    ret = aggregate(use_progressbar=True, **kwargs)
    _print_result(ret, output_keywords_file, output_format)


@cli.command('diff')
@click.argument('keywords1_file_path', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('keywords2_file_path', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-s', '--synonyms-only', default=False, is_flag=True,
              help='Print only changes in synonyms.')
@click.option('-k', '--keywords-only', default=False, is_flag=True,
              help='Print only changes in keywords.')
@click.option('-r', '--regexp-only', default=False, is_flag=True,
              help='Print only changes in regular expressions.')
def cli_diff(keywords1_file_path, keywords2_file_path, synonyms_only=False, keywords_only=False,
             regexp_only=False):
    """Compute diff on keyword files."""
    # pylint: disable=too-many-locals
    if synonyms_only and keywords_only:
        raise ValueError('Cannot use --synonyms-only and --keywords-only at the same time')

    keywords1 = anymarkup.parse_file(keywords1_file_path)
    keywords2 = anymarkup.parse_file(keywords2_file_path)
    differ = False

    for action, keywords_a, keywords_b, file_path in (('Removed', keywords1, keywords2,
                                                       keywords1_file_path),
                                                      ('Added', keywords2, keywords1,
                                                       keywords2_file_path)):
        for keyword, value in keywords_a.items():
            if not synonyms_only and not regexp_only and keyword not in keywords_b.keys():
                print("%s keyword '%s' in file '%s'" % (action, keyword, file_path))
                differ = True
                continue

            if not keywords_only and not regexp_only and value is not None:
                for synonym in (value.get('synonyms') or[]):  # pylint: disable=superfluous-parens
                    if synonym not in keywords_b[keyword].get('synonyms', []):
                        print("%s synonym '%s' for keyword '%s' in file '%s'" %
                              (action, synonym, keyword, file_path))
                        differ = True

            if not keywords_only and not synonyms_only and value is not None:
                for regexp in (value.get('regexp') or []):  # pylint: disable=superfluous-parens
                    if regexp not in keywords_b[keyword].get('regexp', []):
                        print("%s regexp '%s' for keyword '%s' in file '%s'" %
                              (action, regexp, keyword, file_path))
                        differ = True

    if not differ:
        print("Files '%s' and '%s' do not differ" % (keywords1_file_path, keywords2_file_path))


@cli.command('reckon')
@click.option('-o', '--output-file',
              help='Output file with found keywords.')
@click.option('--keywords-file', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to keywords file.')
@click.option('--stopwords-file', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to stopwords file.')
@click.option('-f', '--output-format',
              help='Output keywords format/type.')
@click.option('--stemmer', type=click.Choice(get_registered_stemmers()), multiple=False,
              help='Stemmer type to be used, default: %s.' % defaults.DEFAULT_STEMMER)
@click.option('--lemmatize', is_flag=True,
              help='Use lemmatizer, default: %s' % defaults.DEFAULT_LEMMATIZER)
def cli_reckon(**kwargs):
    """Compute keywords and stopwords based on stemmer and lemmatizer configuration."""
    output_file = kwargs.pop('output_file')
    output_format = kwargs.pop('output_format')
    ret = reckon(**kwargs)
    _print_result(ret, output_file, output_format)


if __name__ == '__main__':
    sys.exit(cli())
