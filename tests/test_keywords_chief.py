"""Tests for the KeywordsChief class."""

import pytest
import io
from f8a_tagger.keywords_chief import KeywordsChief
import f8a_tagger.defaults as defaults
import f8a_tagger.errors


def test_initial_state():
    """Check the initial state of KeywordsChief."""
    keywordsChief = KeywordsChief()
    assert keywordsChief._stemmer == defaults.DEFAULT_STEMMER
    assert keywordsChief._lemmatizer == defaults.DEFAULT_LEMMATIZER
    assert keywordsChief._keywords is not None
    assert keywordsChief._keywords_prop is None


def test_custom_keyword_file_loading():
    """Test if the custom keyword file could be loaded."""
    keywordsChief = KeywordsChief("test_data/keywords.yaml")
    assert keywordsChief._keywords is not None
    assert len(keywordsChief._keywords) == 6


def test_non_existing_keyword_file_loading():
    """Test if non-existing keyword file is properly reported."""
    with pytest.raises(FileNotFoundError) as e:
        keywordsChief = KeywordsChief("test_data/non_existing_file.yaml")


def test_keyword_file_check():
    """Test the checks performed over keyword file."""
    # None is accepted
    keywordsChief1 = KeywordsChief(None)
    assert keywordsChief1._keywords is not None

    # Empty string is accepted as well
    keywordsChief2 = KeywordsChief("")
    assert keywordsChief2._keywords is not None

    # most other types are not accepted
    inputs = [True, False, 42, 1.5, [], {}]
    for keyword_file in inputs:
        with pytest.raises(f8a_tagger.errors.InvalidInputError) as e:
            keywordsChief3 = KeywordsChief(keyword_file)


def test_keyword_loading_from_bytestream():
    """Test the checks performed over keyword file."""
    # bytestream needs to be supported as well
    with open("test_data/keywords.yaml", "r") as fin:
        content = fin.read()
        bytestream = io.BytesIO(content.encode())
        fin = io.TextIOWrapper(bytestream)
        keywordsChief = KeywordsChief(fin)
        assert keywordsChief._keywords is not None


class CustomLemmatizer(object):
    """Custom lemmatizer to be used by following test."""

    def __init__(self):
        """Initialize this dummy class."""
        pass

    def lemmatize(self, x):
        """Lemmatize one word."""
        return x


def test_custom_lemmatizer():
    """Test words loading using custom lemmatizer."""
    custom_lemmatizer = CustomLemmatizer()
    keywordsChief = KeywordsChief("test_data/keywords.yaml", lemmatizer=custom_lemmatizer)
    assert keywordsChief._keywords is not None
    assert len(keywordsChief._keywords) == 6


def test_keywords_property():
    """Check the 'keywords' property."""
    keywordsChief = KeywordsChief("test_data/keywords.yaml")
    keywords = keywordsChief.keywords

    # check that data has been loaded
    assert keywords is not None

    # check all expected values in the map
    expected_keys = ["machine-learning", "django", "url", "python",
                     "functional-programming", "utilities"]
    for expected_key in expected_keys:
        assert expected_key in keywords
        attributes = keywords[expected_key]
        assert "synonyms" in attributes
        assert "occurrence_count" in attributes
        assert attributes["occurrence_count"] == 1

    # test content
    assert keywords["python"]["synonyms"] == ["python"]
    assert sorted(keywords["machine-learning"]["synonyms"]) == \
        sorted(["ml", "machine-learn", "machine-learning"])
    assert keywords["django"]["synonyms"] == ["django"]
    assert keywords["django"]["regexp"] == [".*django.*"]


def test_get_keywords_count_method():
    """Check the get_keywords_count() method."""
    keywordsChief1 = KeywordsChief("test_data/keywords.yaml")
    assert keywordsChief1.get_keywords_count() == 6

    keywordsChief2 = KeywordsChief("test_data/keywords_ngram2.yaml")
    assert keywordsChief2.get_keywords_count() == 6

    keywordsChief3 = KeywordsChief("test_data/keywords_ngram3.yaml")
    assert keywordsChief3.get_keywords_count() == 6


def test_get_average_occurence_count_method():
    """Check the get_average_occurrence_count() method."""
    keywordsChief1 = KeywordsChief("test_data/keywords.yaml")
    assert keywordsChief1.get_average_occurrence_count() == 1.0

    keywordsChief2 = KeywordsChief("test_data/keywords_ngram2.yaml")
    assert keywordsChief2.get_average_occurrence_count() == 1.0

    keywordsChief3 = KeywordsChief("test_data/keywords_ngram3.yaml")
    assert keywordsChief3.get_average_occurrence_count() == 1.0


def test_compute_ngram_size_method():
    """Check the compute_ngram_size() method."""
    keywordsChief1 = KeywordsChief("test_data/keywords.yaml")
    # we expect 1
    assert keywordsChief1.compute_ngram_size() == 1

    keywordsChief2 = KeywordsChief("test_data/keywords_ngram2.yaml")
    # we expect 2 because of synonym 'machine learning'
    assert keywordsChief2.compute_ngram_size() == 2

    keywordsChief3 = KeywordsChief("test_data/keywords_ngram3.yaml")
    # we expect 3 because of synonym 'machine learning algorithms'
    assert keywordsChief3.compute_ngram_size() == 3


def test_get_synonyms_method_positive():
    """Check the get_synonyms() method."""
    keywordsChief = KeywordsChief("test_data/keywords.yaml")
    assert "python" in keywordsChief.get_synonyms("python")
    assert "machine-learning" in keywordsChief.get_synonyms("machine-learning")
    assert "machine-learn" in keywordsChief.get_synonyms("machine-learning")
    assert "ml" in keywordsChief.get_synonyms("machine-learning")


def test_get_synonyms_method_negative():
    """Check the get_synonyms() method."""
    keywordsChief = KeywordsChief("test_data/keywords.yaml")
    assert "XXX" not in keywordsChief.get_synonyms("python")
    assert not keywordsChief.get_synonyms("unknown")
    assert not keywordsChief.get_synonyms("")


def test_get_keyword_method_positive():
    """Check the get_keyword() method."""
    keywordsChief = KeywordsChief("test_data/keywords.yaml")

    expected_keywords = {
        "python": "python",
        "machine-learning": "machine-learning",
        "ml": "machine-learning",
        "urls": "url",
        "django": "django",
        "XXdjango": "django",
        "djangoXX": "django",
        "XXdjangoYY": "django"
    }

    for token, expected_keyword in expected_keywords.items():
        assert keywordsChief.get_keyword(token) == expected_keyword


def test_get_keyword_method_negative():
    """Check the get_keyword() method."""
    keywordsChief = KeywordsChief("test_data/keywords.yaml")

    assert keywordsChief.get_keyword("") is None
    assert keywordsChief.get_keyword(" ") is None
    assert keywordsChief.get_keyword("something_else") is None


def test_extract_keywords():
    """Test the method extract_keywords()."""
    keywordsChief = KeywordsChief("test_data/keywords.yaml")

    assert keywordsChief.extract_keywords([""]) == {}
    assert keywordsChief.extract_keywords(["unknown"]) == {}
    assert keywordsChief.extract_keywords(["python"]) == {"python": 1}
    assert keywordsChief.extract_keywords(["python", "functional-programming", "unknown"]) == \
        {'python': 1, 'functional-programming': 1}
    assert keywordsChief.extract_keywords(["python", "functional-programming", "ml"]) == \
        {'python': 1, 'functional-programming': 1, 'machine-learning': 1}


def test_filter_keywords():
    """Test the static method filter_keyword()."""
    pass
    # TODO: this method seems to be broken
    # print(KeywordsChief.filter_keyword("python"))


def test_compute_synonyms():
    """Test the static method compute_synonyms()."""
    # expected outputs
    f_programming = sorted(["functional programming", "functional/programming",
                            "functional-programming", "functional_programming"])
    immutable_data_type = sorted(["immutable/data/type", "immutable data type",
                                  "immutable-data-type", "immutable_data_type"])

    assert KeywordsChief.compute_synonyms("") == [""]
    assert KeywordsChief.compute_synonyms("python") == ["python"]
    assert sorted(KeywordsChief.compute_synonyms("functional-programming")) == f_programming
    assert sorted(KeywordsChief.compute_synonyms("functional/programming")) == f_programming
    assert sorted(KeywordsChief.compute_synonyms("functional programming")) == f_programming
    assert sorted(KeywordsChief.compute_synonyms("immutable data type")) == immutable_data_type
    assert sorted(KeywordsChief.compute_synonyms("immutable-data-type")) == immutable_data_type
    assert sorted(KeywordsChief.compute_synonyms("immutable/data/type")) == immutable_data_type


def test_is_keyword_positive():
    """Test the method/predicate is_keyword()."""
    keywordsChief = KeywordsChief("test_data/keywords.yaml")
    assert keywordsChief.is_keyword("python")
    assert keywordsChief.is_keyword("machine-learning")


def test_is_keyword_negative():
    """Test the method/predicate is_keyword()."""
    keywordsChief = KeywordsChief("test_data/keywords.yaml")
    assert not keywordsChief.is_keyword("")
    assert not keywordsChief.is_keyword("ml")
    assert not keywordsChief.is_keyword("machine/learning")
    assert not keywordsChief.is_keyword("machine learning")


def test_matches_keyword_pattern_positive():
    """Test the class method matches_keyword_pattern()."""
    assert KeywordsChief.matches_keyword_pattern("python")
    assert KeywordsChief.matches_keyword_pattern("ml")
    assert KeywordsChief.matches_keyword_pattern("functional-programming")
    assert KeywordsChief.matches_keyword_pattern("functional_programming")


def test_matches_keyword_pattern_negative():
    """Test the class method matches_keyword_pattern()."""
    assert not KeywordsChief.matches_keyword_pattern("")
    assert not KeywordsChief.matches_keyword_pattern(" ")
    assert not KeywordsChief.matches_keyword_pattern("???")
    assert not KeywordsChief.matches_keyword_pattern("a^b^c")
    assert not KeywordsChief.matches_keyword_pattern("functional programming")
    assert not KeywordsChief.matches_keyword_pattern("functional&programming")


if __name__ == '__main__':
    test_initial_state()
    test_custom_keyword_file_loading()
    test_non_existing_keyword_file_loading()
    test_keyword_file_check()
    test_keyword_loading_from_bytestream()
    test_keywords_property()
    test_get_keywords_count_method()
    test_get_average_occurence_count_method()
    test_compute_ngram_size_method()
    test_get_synonyms_method_positive()
    test_get_synonyms_method_negative()
    test_get_keyword_method_positive()
    test_get_keyword_method_negative()
    test_extract_keywords()
    test_filter_keywords()
    test_compute_synonyms()
    test_is_keyword_positive()
    test_is_keyword_negative()
    test_matches_keyword_pattern_positive()
    test_matches_keyword_pattern_negative()
    test_custom_lemmatizer()
