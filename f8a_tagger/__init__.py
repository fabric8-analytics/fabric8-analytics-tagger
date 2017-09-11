"""Keyword extraction/tagger for fabric8-analytics."""

__version_info__ = ('0', '1')
__version__ = '.'.join(__version_info__)
__title__ = 'fabric8-analytics-tagger'
__author__ = 'Fridolin Pokorny'
__license__ = 'ASL 2.0'
__copyright__ = 'Copyright 2017 Fridolin Pokorny'

from .corpus import Corpus
from .errors import RemoteDependencyMissingError
from .keywords_chief import KeywordsChief
from .recipes import aggregate
from .recipes import collect
from .recipes import get_registered_collectors
from .recipes import get_registered_scorers
from .recipes import get_registered_stemmers
from .recipes import lookup_file
from .recipes import lookup_readme
from .recipes import lookup_text
from .recipes import reckon
from .tokenizer import Tokenizer


def prepare():
    """Prepare tagger for run - this should be after installation to initialize tagger's resources."""
    import nltk
    import requests
    from libarchive import extract_memory
    import os
    from shutil import move
    from f8a_tagger.utils import get_files_dir

    nltk.download("punkt")
    nltk.download("wordnet")

    maven_index_checker_url = 'https://github.com/fabric8-analytics/' \
                              'maven-index-checker/files/1275145/' \
                              'maven-index-checker-v0.1-alpha.zip'
    response = requests.get(maven_index_checker_url)
    if response.ok is not True:
        raise RemoteDependencyMissingError("Failed to download maven-index-checker with response code %s",
                                           response.status_code)

    # Unfortunately no way how to know name or path of extracted file,
    # so assume it's maven-index-checker.jar
    jar_name = "maven-index-checker.jar"

    jar_path = get_files_dir()
    extract_memory(response.content)
    move(jar_name, os.path.join(jar_path, jar_name))
