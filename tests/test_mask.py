"""Tests für validkit.mask.mask_secret."""

import pytest

from validkit.mask import mask_secret


def test_masks_all_but_last_keep_characters():
    assert mask_secret("geheim", keep=2) == "****im"


def test_short_string_stays_fully_visible_with_default_keep():
    assert mask_secret("abc") == "abc"


def test_keep_equal_to_length_keeps_whole_string():
    assert mask_secret("geheim", keep=6) == "geheim"


def test_keep_greater_than_length_keeps_whole_string():
    assert mask_secret("abc", keep=5) == "abc"


def test_keep_zero_masks_everything():
    assert mask_secret("geheim", keep=0) == "******"


def test_negative_keep_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("geheim", keep=-1)


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        mask_secret(12345)


def test_non_int_keep_raises_type_error():
    with pytest.raises(TypeError):
        mask_secret("geheim", keep=2.5)


def test_text_at_maximum_length_is_accepted():
    assert mask_secret("x" * 1000) == "*" * 996 + "xxxx"


def test_text_over_maximum_length_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("x" * 1001)


def test_error_messages_do_not_contain_input_values():
    secret = "supergeheim"
    with pytest.raises(ValueError) as exc_info:
        mask_secret(secret, keep=-1)
    assert secret not in str(exc_info.value)

    with pytest.raises(TypeError) as exc_info:
        mask_secret(12345)
    assert "12345" not in str(exc_info.value)
