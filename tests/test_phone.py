"""Tests für validkit.phone.normalize_phone."""

import time

import pytest

from validkit.phone import normalize_phone


def test_local_number_gets_country_code():
    assert normalize_phone("030 1234567", "49") == "+49301234567"


def test_international_plus_prefix():
    assert normalize_phone("+49 170 1234567", "49") == "+491701234567"


def test_international_double_zero_prefix():
    assert normalize_phone("0049 170 1234567", "49") == "+491701234567"


def test_separators_are_removed():
    assert normalize_phone("(030) 123-4567.", "49") == "+49301234567"


def test_invalid_characters_raise_valueerror():
    with pytest.raises(ValueError):
        normalize_phone("030 1234abc", "49")


def test_empty_national_part_raises_valueerror():
    with pytest.raises(ValueError):
        normalize_phone("", "49")
    with pytest.raises(ValueError):
        normalize_phone("   ", "49")
    with pytest.raises(ValueError):
        normalize_phone("+", "49")


def test_wrong_type_raises_typeerror():
    with pytest.raises(TypeError):
        normalize_phone(12345, "49")
    with pytest.raises(TypeError):
        normalize_phone("030 1234567", 49)


def test_over_1000_chars_rejected():
    with pytest.raises(ValueError):
        normalize_phone("1" * 1001, "49")


def test_10000_char_input_finishes_under_100ms():
    start = time.perf_counter()
    with pytest.raises(ValueError):
        normalize_phone("1" * 10000, "49")
    assert time.perf_counter() - start < 0.1


def test_error_messages_do_not_contain_input():
    bad = "030 1234abc"
    with pytest.raises(ValueError) as exc:
        normalize_phone(bad, "49")
    assert bad not in str(exc.value)
