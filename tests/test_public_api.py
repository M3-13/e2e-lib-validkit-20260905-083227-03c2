"""Testet die öffentliche API von validkit: genau neun exportierte Funktionen mit den
vereinbarten Signaturen. Das Verhalten der Funktionen selbst testen die jeweils
eigenen Tests in tests/test_<modul>.py."""

import inspect

import validkit

EXPECTED_SIGNATURES = {
    "is_valid_email": "(text: str) -> bool",
    "luhn_check": "(digits: str | int) -> bool",
    "is_valid_isbn13": "(text: str) -> bool",
    "is_valid_iban": "(text: str) -> bool",
    "normalize_phone": "(text: str, country_code: str) -> str",
    "strip_accents": "(text: str) -> str",
    "mask_secret": "(text: str, keep: int = 4) -> str",
    "slugify": "(text: str) -> str",
    "clamp": "(value: int | float, low: int | float, high: int | float) -> int | float",
}


def test_public_api_exports_exactly_nine_functions():
    assert set(validkit.__all__) == set(EXPECTED_SIGNATURES)

    for name in EXPECTED_SIGNATURES:
        func = getattr(validkit, name)
        assert callable(func), f"{name} ist nicht aufrufbar"


def test_public_api_signatures_match_contract():
    for name, expected in EXPECTED_SIGNATURES.items():
        func = getattr(validkit, name)
        assert str(inspect.signature(func)) == expected, f"{name}: falsche Signatur"
