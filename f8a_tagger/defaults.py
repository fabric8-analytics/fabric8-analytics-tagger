#!/usr/bin/env python3
"""Default values and configuration."""

# Possible word delimiters for synonyms.
MULTIWORD_DELIMITERS = (' ', '-', '_', '/')

# Default output format if not explicitly stated.
DEFAULT_OUTPUT_FORMAT = 'yaml'

# Stemmer to be used by default.
DEFAULT_STEMMER = None
# DEFAULT_STEMMER = Stemmer.get_stemmer('EnglishStemmer')

# Lemmatizer to be used by default.
DEFAULT_LEMMATIZER = None
# DEFAULT_LEMMATIZER = Lemmatizer.get_lemmatizer()

# Filter keywords that have low occurrence.
OCCURRENCE_COUNT_FILTER = 2
