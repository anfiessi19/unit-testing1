import pytest

from text_utils import analyze_text


def test_returns_all_expected_keys():
    result = analyze_text("Hello world")
    assert set(result) == {
        "word_count",
        "unique_words",
        "longest_word",
        "average_word_length",
        "most_common_letter",
    }


def test_basic_text():
    result = analyze_text("Hello world")
    assert result == {
        "word_count": 2,
        "unique_words": 2,
        "longest_word": "Hello",  # при однаковій довжині - перше слово
        "average_word_length": 5.0,
        "most_common_letter": "l",
    }


def test_repeated_words_and_most_common_letter():
    result = analyze_text("the cat and the hat")
    assert result["word_count"] == 5
    assert result["unique_words"] == 4
    assert result["longest_word"] == "the"
    assert result["average_word_length"] == 3.0
    assert result["most_common_letter"] == "t"


@pytest.mark.parametrize("text", ["", "   ", "\n\t  "])
def test_empty_or_whitespace_text_raises(text):
    with pytest.raises(ValueError, match="порожнім"):
        analyze_text(text)


def test_punctuation_is_stripped_from_word_edges():
    result = analyze_text("Hello, world!")
    assert result["word_count"] == 2
    assert result["longest_word"] == "Hello"
    assert result["average_word_length"] == 5.0


def test_standalone_punctuation_tokens_are_ignored():
    result = analyze_text("Hello ... world")
    assert result["word_count"] == 2
    assert result["unique_words"] == 2


def test_unique_words_is_case_insensitive():
    result = analyze_text("Python python PYTHON")
    assert result["word_count"] == 3
    assert result["unique_words"] == 1
    assert result["average_word_length"] == 6.0


def test_longest_word_keeps_original_case():
    result = analyze_text("a Bigword")
    assert result["longest_word"] == "Bigword"


def test_average_word_length_is_rounded_to_two_decimals():
    result = analyze_text("a b cc")  # 4 / 3 = 1.333...
    assert result["average_word_length"] == 1.33


def test_inner_hyphen_and_apostrophe_are_preserved():
    result = analyze_text("well-known don't")
    assert result["word_count"] == 2
    assert result["longest_word"] == "well-known"
    assert result["average_word_length"] == 7.5


def test_multiple_whitespace_and_newlines():
    result = analyze_text("one\ntwo   three")
    assert result["word_count"] == 3
    assert result["longest_word"] == "three"


def test_digits_count_as_words_but_not_as_letters():
    result = analyze_text("123 456")
    assert result["word_count"] == 2
    assert result["average_word_length"] == 3.0
    assert result["most_common_letter"] is None


def test_most_common_letter_ignores_case():
    result = analyze_text("Aa a b")
    assert result["most_common_letter"] == "a"


def test_most_common_letter_tie_returns_one_of_candidates():
    # у разі нічиєї max() по set не гарантує детермінованого результату
    result = analyze_text("ab")
    assert result["most_common_letter"] in {"a", "b"}


def test_cyrillic_text():
    result = analyze_text("Привіт світ")
    assert result["word_count"] == 2
    assert result["unique_words"] == 2
    assert result["longest_word"] == "Привіт"
    assert result["average_word_length"] == 5.0
    assert result["most_common_letter"] in {"в", "і", "т"}


def test_only_punctuation_raises_value_error():
    # поточна поведінка: max() кидає ValueError на порожній послідовності
    with pytest.raises(ValueError):
        analyze_text("... !!!")