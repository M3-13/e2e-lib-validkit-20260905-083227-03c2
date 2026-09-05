"""Tests für validkit.luhn.luhn_check: Luhn-Prüfsumme inklusive Grenz- und Fehlerfällen."""

import pytest

from validkit.luhn import luhn_check


def test_valid_check_digit_string_returns_true():
    assert luhn_check("79927398713") is True


def test_invalid_check_digit_string_returns_false():
    assert luhn_check("79927398712") is False


def test_valid_int_input_returns_true():
    assert luhn_check(79927398713) is True


def test_invalid_int_input_returns_false():
    assert luhn_check(79927398712) is False


def test_shortest_valid_two_digit_sequence():
    assert luhn_check("00") is True


def test_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("")


def test_single_digit_string_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("7")


def test_single_digit_int_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check(7)


def test_zero_int_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check(0)


def test_non_digit_string_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("7992739871A")


def test_letter_only_string_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("abc")


def test_string_with_whitespace_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("7992 7398713")


def test_negative_int_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check(-79927398713)


def test_none_raises_type_error():
    with pytest.raises(TypeError):
        luhn_check(None)


def test_float_raises_type_error():
    with pytest.raises(TypeError):
        luhn_check(79927398713.0)


def test_bool_raises_type_error():
    with pytest.raises(TypeError):
        luhn_check(True)


def test_list_raises_type_error():
    with pytest.raises(TypeError):
        luhn_check(["7", "9"])


def test_string_over_1000_characters_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("1" * 1001)


def test_string_of_exactly_1000_characters_is_processed():
    assert isinstance(luhn_check("1" * 1000), bool)


def test_error_messages_do_not_contain_input_values():
    invalid = "7992739871X"
    with pytest.raises(ValueError) as exc:
        luhn_check(invalid)
    assert invalid not in str(exc.value)

    too_long = "1" * 1001
    with pytest.raises(ValueError) as exc:
        luhn_check(too_long)
    assert too_long not in str(exc.value)
