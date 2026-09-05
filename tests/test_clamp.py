"""Unit-Tests für validkit.clamp.clamp."""

import pytest

from validkit import clamp


def test_clamp_within_range_returns_value():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_low_returns_low():
    assert clamp(-5, 0, 10) == 0


def test_clamp_above_high_returns_high():
    assert clamp(15, 0, 10) == 10


def test_clamp_at_boundaries_returns_boundary():
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10


def test_clamp_float_values():
    assert clamp(3.7, 0.0, 10.0) == 3.7
    assert clamp(-1.5, 0.0, 10.0) == 0.0
    assert clamp(12.5, 0.0, 10.0) == 10.0


def test_clamp_mixed_int_and_float():
    assert clamp(15, 0.0, 10.0) == 10.0
    assert clamp(3.2, 0, 10) == 3.2


def test_clamp_low_greater_than_high_raises_value_error():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)


def test_clamp_non_numeric_value_raises_type_error():
    with pytest.raises(TypeError):
        clamp("5", 0, 10)


def test_clamp_non_numeric_bounds_raise_type_error():
    with pytest.raises(TypeError):
        clamp(5, "0", 10)
    with pytest.raises(TypeError):
        clamp(5, 0, "10")


def test_clamp_rejects_bool():
    with pytest.raises(TypeError):
        clamp(True, 0, 10)


def test_clamp_error_messages_do_not_contain_input_values():
    with pytest.raises(ValueError) as exc_info:
        clamp(5, 10, 0)
    message = str(exc_info.value)
    assert "5" not in message
    assert "10" not in message

    with pytest.raises(TypeError) as exc_info:
        clamp("secret-value", 0, 10)
    assert "secret-value" not in str(exc_info.value)
