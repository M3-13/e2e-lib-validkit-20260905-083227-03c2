"""Tests für validkit.slug.slugify."""

import time

import pytest

from validkit.slug import slugify


def test_slugify_removes_accents_and_special_chars():
    assert slugify("Héllo Wörld!") == "hello-world"


def test_slugify_collapses_repeated_hyphens_and_strips_edges():
    assert slugify("  Hello   Wörld  ") == "hello-world"


def test_slugify_only_special_chars_raises_value_error():
    with pytest.raises(ValueError):
        slugify("!!!###")


def test_slugify_non_string_raises_type_error():
    with pytest.raises(TypeError):
        slugify(123)
    with pytest.raises(TypeError):
        slugify(None)


def test_slugify_rejects_long_input_before_processing():
    with pytest.raises(ValueError):
        slugify("a" * 1001)


def test_slugify_error_messages_do_not_contain_input():
    secret = "top-secret-value"
    with pytest.raises(ValueError) as excinfo:
        slugify(secret * 200)
    assert secret not in str(excinfo.value)


def test_slugify_ten_thousand_chars_completes_quickly():
    start = time.perf_counter()
    with pytest.raises(ValueError):
        slugify("!" * 10000)
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1
