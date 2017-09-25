#!/usr/bin/env python3
"""Keywords extraction/tagging for fabric8-analytics."""

from itertools import chain
import os

import anymarkup
import daiquiri
from f8a_tagger.collectors import CollectorBase
import f8a_tagger.defaults as defaults
from f8a_tagger.errors import InvalidInputError
from f8a_tagger.keywords_chief import KeywordsChief
from f8a_tagger.keywords_set import KeywordsSet
from f8a_tagger.lemmatizer import Lemmatizer
from f8a_tagger.parsers import CoreParser
from f8a_tagger.scoring import Scoring
from f8a_tagger.stemmer import Stemmer
from f8a_tagger.tokenizer import Tokenizer
from f8a_tagger.utils import iter_files
from f8a_tagger.utils import progressbarize

_logger = daiquiri.getLogger(__name__)


def _prepare_lookup(keywords_file=None, stopwords_file=None, ngram_size=None, lemmatize=False,
                    stemmer=None):
    # pylint: disable=too-many-arguments
    """Prepare resources for keywords lookup.

    :param keywords_file: keywords file to be used
    :param stopwords_file: stopwords file to be used
    :param ngram_size: size of ngrams, if None, ngram size is computed
    :param lemmatize: use lemmatizer
    :type lemmatize: bool
    :param stemmer: stemmer to be used
    :type stemmer: str
    """
    stemmer_instance = Stemmer.get_stemmer(stemmer) if stemmer is not None else None
    lemmatizer_instance = Lemmatizer.get_lemmatizer() if lemmatize else None

    chief = KeywordsChief(keywords_file, lemmatizer=lemmatizer_instance, stemmer=stemmer_instance)
    computed_ngram_size = chief.compute_ngram_size()
    if ngram_size is not None and computed_ngram_size > ngram_size:
        _logger.warning("Computed ngram size (%d) does not reflect supplied ngram size (%d), "
                        "some synonyms will be omitted", chief.compute_ngram_size(), ngram_size)
    elif ngram_size is None:
        ngram_size = computed_ngram_size

    tokenizer = Tokenizer(stopwords_file, ngram_size, lemmatizer=lemmatizer_instance,
                          stemmer=stemmer_instance)

    return ngram_size, tokenizer, chief, CoreParser()


def _perform_lookup(content, tokenizer, chief, scorer):
    """Perform actual keyword lookup.

    :param content: content on which keyword lookup should be performed
    :param tokenizer: tokenizer instance to be used
    :param chief: keywords chief instance to be used
    :param scorer: name of scorer to be used
    :type scorer: str
    """
    tokens = tokenizer.tokenize(content)
    # We do not perform any analysis on sentences now, so treat all tokens as
    # one array (sentences of tokens).
    tokens = chain(*tokens)
    keywords = chief.extract_keywords(tokens)
    scorer = Scoring.get_scoring(scorer or defaults.DEFAULT_SCORER)
    return scorer.score(chief, keywords)


def lookup_file(path, keywords_file=None, stopwords_file=None,
                ignore_errors=False, ngram_size=None, use_progressbar=False,
                lemmatize=False, stemmer=None, scorer=None):
    # pylint: disable=too-many-arguments,too-many-locals
    """Perform keywords lookup on a file or directory tree of files.

    :param path: path of directory tree or file on which the lookup should be done
    :param keywords_file: keywords file to be used
    :param stopwords_file: stopwords file to be used
    :param ignore_errors: True, if errors should be reported but computation shouldn't be stopped
    :param ngram_size: size of ngrams, if None, ngram size is computed
    :param use_progressbar: True if progressbar should be shown
    :param lemmatize: use lemmatizer
    :type lemmatize: bool
    :param stemmer: stemmer to be used
    :type stemmer: str
    :param scorer: scorer to be used
    :type scorer: f8a_tagger.scoring.Scoring
    :return: found keywords, reported per file
    """
    ret = {}
    ngram_size, tokenizer, chief, core_parser = _prepare_lookup(keywords_file,
                                                                stopwords_file,
                                                                ngram_size,
                                                                lemmatize,
                                                                stemmer)
    for project, file in progressbarize(iter_files(path, ignore_errors), progress=use_progressbar):
        file_name = file
        if not isinstance(file, str):
            file_name = file.name
        _logger.info("Processing file '%s' for project '%s'", file_name, project)
        try:
            content = core_parser.parse_file(file_name)
            keywords = _perform_lookup(content, tokenizer, chief, scorer)
        except Exception as exc:  # pylint: disable=broad-except
            if not ignore_errors:
                raise
            _logger.exception("Failed to parse content in file '%s': %s", file_name, str(exc))
            continue
        finally:
            # Remove temporary file here so we can use safely progressbar
            if not isinstance(file, str):
                _logger.debug("Removing temporary file '%s' for project '%s'", file_name, project)
                os.remove(file_name)

        ret[project] = keywords

    return ret


def lookup_readme(readme, keywords_file=None, stopwords_file=None, ngram_size=None,
                  lemmatize=False, stemmer=None, scorer=None):
    # pylint: disable=too-many-arguments
    """Perform keywords lookup in a parsed README.json dict.

    :param readme: parsed README.json file
    :param keywords_file: keywords file to be used
    :param stopwords_file: stopwords file to be used
    :param ngram_size: size of ngrams, if None, ngram size is computed
    :param lemmatize: use lemmatizer
    :type lemmatize: bool
    :param stemmer: stemmer to be used
    :type stemmer: str
    :param scorer: scorer to be used
    :type scorer: f8a_tagger.scoring.Scoring
    :return: found keywords
    """
    ngram_size, tokenizer, chief, core_parser = _prepare_lookup(keywords_file,
                                                                stopwords_file,
                                                                ngram_size,
                                                                lemmatize,
                                                                stemmer)
    if not isinstance(readme, dict):
        raise InvalidInputError("Invalid README passed '%s' (type: %s), should be dict or JSON"
                                % (readme, type(readme)))

    content = readme.get('content')
    content_type = readme.get('type')
    if not content:
        raise InvalidInputError("No content provided in README: '%s'" % readme)
    if not content_type:
        raise InvalidInputError("No content type provided in README.json")

    return _perform_lookup(core_parser.parse(content, content_type), tokenizer, chief, scorer)


def lookup_text(text, keywords_file=None, stopwords_file=None, ngram_size=None,
                lemmatize=False, stemmer=None, scorer=None):
    # pylint: disable=too-many-arguments
    """Perform keywords lookup on a plain text.

    :param text: plain text on which keywords lookup should be performed
    :param keywords_file: keywords file to be used
    :param stopwords_file: stopwords file to be used
    :param ngram_size: size of ngrams, if None, ngram size is computed
    :param lemmatize: use lemmatizer
    :type lemmatize: bool
    :param stemmer: stemmer to be used
    :type stemmer: str
    :param scorer: scorer to be used
    :type scorer: f8a_tagger.scoring.Scoring
    :return: found keywords
    """
    ngram_size, tokenizer, chief, core_parser = _prepare_lookup(keywords_file,
                                                                stopwords_file,
                                                                ngram_size,
                                                                lemmatize,
                                                                stemmer)
    if not isinstance(text, str):
        raise InvalidInputError("Invalid text passed '%s' (type: %s), should be string" %
                                (text, type(text)))
    return _perform_lookup(core_parser.parse(text, 'txt'), tokenizer, chief, scorer)


def collect(collector=None, ignore_errors=False, use_progressbar=False):
    """Collect keywords from external resources.

    :param collector: a list/tuple of collectors to be used
    :param ignore_errors: if True, ignore all errors, but report them
    :param use_progressbar: use progressbar if True
    :return: all collected keywords
    """
    keywords_set = KeywordsSet()
    for col in (collector or CollectorBase.get_registered_collectors()):
        # pylint: disable=superfluous-parens
        try:
            collector_instance = CollectorBase.get_collector_class(col)()
            keywords_set.union(collector_instance.execute(ignore_errors, use_progressbar))
        except Exception as exc:
            if ignore_errors:
                _logger.exception("Collection of keywords for '%s' failed: %s" % (col, str(exc)))
                continue
            raise

    return keywords_set.keywords


def aggregate(input_keywords_file, no_synonyms=None, use_progressbar=False,
              occurrence_count_filter=None):
    # pylint: disable=too-many-branches
    """Aggregate available topics.

    :param input_keywords_file: a list/tuple of input keywords files to process
    :param no_synonyms: do not compute synonyms for keywords
    :param use_progressbar: use progressbar to report progress
    :param occurrence_count_filter: filter out keywords with low occurrence count
    :return:
    """
    if not input_keywords_file:
        raise ValueError('No input keywords files provided')

    occurrence_count_filter = occurrence_count_filter or 0

    all_keywords = {}
    for input_file in progressbarize(input_keywords_file or [], use_progressbar):
        input_content = anymarkup.parse_file(input_file)
        for keyword, value in input_content.items():
            keyword = str(keyword)

            if not KeywordsChief.matches_keyword_pattern(keyword):
                _logger.debug("Dropping keyword '%s' as it does not match keyword pattern.",
                              keyword)
                continue

            if keyword in all_keywords.keys() and value is not None and \
               all_keywords[keyword] is not None:
                all_keywords[keyword]['occurrence_count'] = \
                    value.pop('occurrence_count', 0) + \
                    all_keywords[keyword].get('occurrence_count', 0)
                for conf, items in value.items():
                    all_keywords[keyword][str(conf)] = list(
                        set(items or []) | set(all_keywords[keyword][str(conf)] or []))
            else:
                all_keywords[keyword] = value if value is not None else {}

            if not no_synonyms:
                synonyms = list(set(all_keywords[keyword].get('synonyms') or []) |
                                set(KeywordsChief.compute_synonyms(keyword)))

                if synonyms:
                    if all_keywords[str(keyword)] is None:
                        all_keywords[str(keyword)] = {}
                    all_keywords[str(keyword)]['synonyms'] = synonyms

    # filter out keywords with low occurrence count
    if occurrence_count_filter > 1:
        result = {}
        for keyword, value in all_keywords.items():
            if value.get('occurrence_count', 1) > occurrence_count_filter:
                result[keyword] = value

        return result

    return all_keywords


def reckon(keywords_file=None, stopwords_file=None, stemmer=None, lemmatize=False):
    """Compute keywords and stopwords based on stemmer and lemmatizer configuration.

    :param keywords_file: keywords file to be used
    :param stopwords_file: stopwords file to be used
    :param stemmer: stemmer to be used
    :param lemmatize: True if lemmatization should be done
    :return: computed keywords and stopwords, duplicit entries are not removed
    """
    result = dict.fromkeys(('keywords', 'stopwords'))

    stemmer_instance = Stemmer.get_stemmer(stemmer) if stemmer is not None else None
    lemmatizer_instance = Lemmatizer.get_lemmatizer() if lemmatize else None

    chief = KeywordsChief(keywords_file, lemmatizer=lemmatizer_instance, stemmer=stemmer_instance)
    tokenizer = Tokenizer(stopwords_file, lemmatizer=lemmatizer_instance, stemmer=stemmer_instance)

    result['keywords'] = chief.keywords
    result['stopwords'] = sorted(tokenizer.raw_stopwords) + sorted(tokenizer.regexp_stopwords)

    return result


def get_registered_collectors():
    """Get all registered collectors."""
    return CollectorBase.get_registered_collectors()


def get_registered_stemmers():
    """Get all stemmers that are available in NLTK."""
    return Stemmer.get_registered_stemmers()


def get_registered_scorers():
    """Get all keyword scorers that are supported."""
    return Scoring.get_registered_scorers()
