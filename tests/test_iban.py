"""Tests für validkit.iban.is_valid_iban."""

import time

import pytest

from validkit.iban import is_valid_iban


def test_valid_german_iban():
    assert is_valid_iban("DE89 3704 0044 0532 0130 00") is True


def test_modified_check_digit_is_invalid():
    assert is_valid_iban("DE88 3704 0044 0532 0130 00") is False


def test_valid_gb_iban():
    assert is_valid_iban("GB82 WEST 1234 5698 7654 32") is True


def test_invalid_country_code_raises():
    with pytest.raises(ValueError):
        is_valid_iban("ZZ89 3704 0044 0532 0130 00")


def test_lowercase_raises():
    with pytest.raises(ValueError):
        is_valid_iban("de89 3704 0044 0532 0130 00")


def test_punctuation_raises():
    with pytest.raises(ValueError):
        is_valid_iban("DE89-3704 0044 0532 0130 00")


def test_too_short_raises():
    with pytest.raises(ValueError):
        is_valid_iban("DE89 3704 0044")


def test_wrong_length_raises():
    with pytest.raises(ValueError):
        is_valid_iban("DE89 3704 0044 0532 0130 0000")


def test_empty_string_raises():
    with pytest.raises(ValueError):
        is_valid_iban("")


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_iban(12345)
    with pytest.raises(TypeError):
        is_valid_iban(None)


def test_over_max_length_raises():
    with pytest.raises(ValueError):
        is_valid_iban("A" * 1001)


def test_ten_thousand_chars_completes_quickly():
    text = "A" * 10000
    start = time.perf_counter()
    with pytest.raises(ValueError):
        is_valid_iban(text)
    assert time.perf_counter() - start < 0.1


def test_error_message_does_not_leak_input():
    secret = "DE89 3704 0044 0532 0130 00"
    with pytest.raises(ValueError) as exc:
        is_valid_iban(secret + "!")
    assert secret not in str(exc.value)
