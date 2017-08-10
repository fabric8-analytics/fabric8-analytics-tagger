#!/usr/bin/env python3
"""Keywords extraction/tagging for fabric8-analytics."""

import anymarkup
import daiquiri
from f8a_tagger.collectors import CollectorBase
from f8a_tagger.keywords_chief import KeywordsChief
from f8a_tagger.keywords_set import KeywordsSet
from f8a_tagger.lemmatizer import Lemmatizer
from f8a_tagger.parsers import CoreParser
from f8a_tagger.stemmer import Stemmer
from f8a_tagger.tokenizer import Tokenizer
from f8a_tagger.utils import iter_files
from f8a_tagger.utils import progressbarize

_logger = daiquiri.getLogger(__name__)


def lookup(path, keywords_file=None, stopwords_file=None,
           ignore_errors=False, ngram_size=None, use_progressbar=False, lemmatize=False, stemmer=None):
    # pylint: disable=too-many-arguments
    """Perform keywords lookup.

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
    :return: found keywords, reported per file
    """
    ret = {}

    chief = KeywordsChief(keywords_file, lemmatizer=lemmatizer_instance, stemmer=stemmer_instance)
    computed_ngram_size = chief.compute_ngram_size()
    if ngram_size is not None and computed_ngram_size > ngram_size:
        _logger.warning("Computed ngram size (%d) does not reflect supplied ngram size (%d), "
                        "some synonyms will be omitted", chief.compute_ngram_size(), ngram_size)
    elif ngram_size is None:
        ngram_size = computed_ngram_size

    stemmer_instance = Stemmer.get_stemmer(stemmer) if stemmer is not None else None
    lemmatizer_instance = Lemmatizer.get_lemmatizer() if lemmatize else None
    tokenizer = Tokenizer(stopwords_file, ngram_size, lemmatizer=lemmatizer_instance, stemmer=stemmer_instance)

    for file in progressbarize(iter_files(path, ignore_errors), progress=use_progressbar):
        _logger.info("Processing file '%s'", file)
        try:
            content = CoreParser().parse_file(file)
            tokens = tokenizer.tokenize(content)
            keywords = chief.extract_keywords(tokens)
        except Exception as exc:  # pylint: disable=broad-except
            if not ignore_errors:
                raise
            _logger.exception("Failed to parse content in file '%s': %s", file, str(exc))
            continue

        ret[file] = keywords

    return ret


def collect(collector=None, ignore_errors=False, use_progressbar=False):
    """Collect keywords from external resources.

    :param collector: a list/tuple of collectors to be used
    :param ignore_errors: if True, ignore all errors, but report them
    :param use_progressbar: use progressbar if True
    :return: all collected keywords
    """
    keywords_set = KeywordsSet()
    for col in (collector or CollectorBase.get_registered_collectors()):  # pylint: disable=superfluous-parens
        try:
            collector_instance = CollectorBase.get_collector_class(col)()
            keywords_set.union(collector_instance.execute(ignore_errors, use_progressbar))
        except Exception as exc:
            if ignore_errors:
                _logger.exception("Collection of keywords for '%s' failed: %s" % (col, str(exc)))
                continue
            raise

    return keywords_set.keywords


def aggregate(input_keywords_file, no_synonyms=None, use_progressbar=False):
    """Aggregate available topics.

    :param input_keywords_file: a list/tuple of input keywords files to process
    :param no_synonyms: do not compute synonyms for keywords
    :param use_progressbar: use progressbar to report progress
    :return:
    """
    if not input_keywords_file:
        raise ValueError('No input keywords files provided')

    all_keywords = {}
    for input_file in progressbarize(input_keywords_file or [], use_progressbar):
        input_content = anymarkup.parse_file(input_file)
        for keyword, value in input_content.items():
            keyword = str(keyword)
            if keyword in all_keywords.keys() and value is not None and all_keywords[keyword] is not None:
                all_keywords[keyword]['occurrence_count'] = value.pop('occurrence_count', 0) +\
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

    return all_keywords


def tf_idf(path):
    """Compute TF-IDF on the given corpus described by directory tree."""
    raise NotImplementedError("Computing TF-IDF is currently not supported")


def get_registered_collectors():
    """Get all registered collectors."""
    return CollectorBase.get_registered_collectors()


def get_registered_stemmers():
    """Get all stemmers that are available in NLTK."""
    return Stemmer.get_registered_stemmers()
