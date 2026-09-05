"""Tests für validkit.email.is_valid_email: Normal-, Grenz- und Fehlerfälle."""

import time

import pytest

from validkit.email import is_valid_email


def test_valid_simple_address():
    assert is_valid_email("user@example.com") is True


def test_valid_with_subdomain():
    assert is_valid_email("user@sub.example.com") is True


def test_valid_with_dot_in_local_part():
    assert is_valid_email("first.last@example.com") is True


def test_valid_with_plus_in_local_part():
    assert is_valid_email("user+tag@example.com") is True


def test_valid_with_hyphen_in_domain():
    assert is_valid_email("user@my-domain.com") is True


def test_invalid_missing_domain():
    assert is_valid_email("user@") is False


def test_invalid_double_at():
    assert is_valid_email("user@@example.com") is False


def test_invalid_domain_without_dot():
    assert is_valid_email("user@example") is False


def test_invalid_missing_local_part():
    assert is_valid_email("@example.com") is False


def test_invalid_leading_dot_in_local_part():
    assert is_valid_email(".user@example.com") is False


def test_invalid_trailing_dot_in_local_part():
    assert is_valid_email("user.@example.com") is False


def test_invalid_consecutive_dots_in_local_part():
    assert is_valid_email("user..name@example.com") is False


def test_invalid_consecutive_dots_in_domain():
    assert is_valid_email("user@example..com") is False


def test_invalid_leading_dot_in_domain():
    assert is_valid_email("user@.example.com") is False


def test_invalid_trailing_dot_in_domain():
    assert is_valid_email("user@example.com.") is False


def test_invalid_space():
    assert is_valid_email("user name@example.com") is False


def test_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_email("")


def test_wrong_type_raises_type_error():
    for value in (None, 42, 3.14, ["user@example.com"], {"a": 1}, b"user@example.com"):
        with pytest.raises(TypeError):
            is_valid_email(value)


def test_length_over_limit_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_email("a" * 1001)


def test_length_at_limit_is_not_rejected_for_length():
    # Genau 1000 Zeichen unterliegen nicht der Längenprüfung, sind aber syntaktisch ungültig.
    assert is_valid_email("a" * 1000) is False


def test_value_error_message_does_not_leak_input():
    distinctive = "top-secret-12345@example.com"
    with pytest.raises(ValueError) as excinfo:
        is_valid_email(distinctive * 40)
    assert distinctive not in str(excinfo.value)


def test_type_error_message_does_not_leak_input():
    with pytest.raises(TypeError) as excinfo:
        is_valid_email(123456789)
    assert "123456789" not in str(excinfo.value)


def test_long_non_matching_input_completes_quickly():
    # AC-14: 10.000 Zeichen lange, nicht passende Eingabe schließt unter 100 ms ab.
    long_input = "a" * 10_000
    start = time.perf_counter()
    with pytest.raises(ValueError):
        is_valid_email(long_input)
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1


def test_regex_resists_catastrophic_backtracking():
    # Nahezu passende, lange Eingabe unterhalb der Längengrenze: die Regex
    # darf nicht explodieren (AC-14).
    tricky = "a" * 900 + "@" + "a" * 90 + "."
    start = time.perf_counter()
    result = is_valid_email(tricky)
    elapsed = time.perf_counter() - start
    assert result is False
    assert elapsed < 0.1
