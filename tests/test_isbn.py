"""Tests für validkit.isbn.is_valid_isbn13."""

import time

import pytest

from validkit.isbn import is_valid_isbn13


def test_valid_isbn13_returns_true():
    assert is_valid_isbn13("978-3-16-148410-0") is True


def test_valid_isbn13_with_spaces():
    assert is_valid_isbn13("978 3 16 148410 0") is True


def test_valid_isbn13_without_separators():
    assert is_valid_isbn13("9783161484100") is True


def test_wrong_check_digit_returns_false():
    assert is_valid_isbn13("978-3-16-148410-1") is False


def test_empty_input_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_isbn13("")


def test_whitespace_only_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_isbn13("   ")


def test_non_digit_character_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_isbn13("978-3-16-14841X-0")


def test_wrong_length_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_isbn13("978-3-16-148410")


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_isbn13(9783161484100)


def test_input_over_max_length_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_isbn13("9" * 1001)


def test_error_messages_do_not_contain_input():
    for bad in ["978-3-16-14841X-0", "978-3-16-148410", "9" * 1001]:
        with pytest.raises(ValueError) as exc_info:
            is_valid_isbn13(bad)
        assert bad not in str(exc_info.value)


def test_ten_thousand_char_input_finishes_quickly():
    start = time.perf_counter()
    with pytest.raises(ValueError):
        is_valid_isbn13("9" * 10_000)
    assert time.perf_counter() - start < 0.1
