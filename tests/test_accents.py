"""Tests fuer validkit.accents.strip_accents."""

import pytest

from validkit.accents import strip_accents


def test_muenchen_strips_umlaut():
    assert strip_accents("München") == "Munchen"


def test_cafe_strips_accent():
    assert strip_accents("café") == "cafe"


def test_combining_character_is_removed():
    # "e" gefolgt von kombinierendem Akut-Akzent (U+0301).
    assert strip_accents("e\u0301") == "e"


def test_mixed_ascii_unchanged():
    assert strip_accents("Hello World") == "Hello World"


def test_multiple_accents():
    assert strip_accents("hétérogénéité") == "heterogeneite"


def test_empty_string():
    assert strip_accents("") == ""


def test_non_string_raises_type_error():
    for value in (None, 42, 3.14, ["München"], {"a": 1}):
        with pytest.raises(TypeError):
            strip_accents(value)


def test_length_limit_boundary():
    # Genau 1000 Zeichen sind erlaubt.
    assert strip_accents("a" * 1000) == "a" * 1000


def test_length_over_limit_raises_value_error():
    with pytest.raises(ValueError):
        strip_accents("a" * 1001)


def test_type_error_message_does_not_leak_input():
    secret = ["top-secret-wert"]
    with pytest.raises(TypeError) as excinfo:
        strip_accents(secret)
    assert "top-secret-wert" not in str(excinfo.value)


def test_length_error_message_does_not_leak_input():
    long_text = "X" * 1001
    with pytest.raises(ValueError) as excinfo:
        strip_accents(long_text)
    assert long_text not in str(excinfo.value)
    assert "1001" not in str(excinfo.value)
