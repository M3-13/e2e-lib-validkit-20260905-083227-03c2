"""IBAN-Validierung nach ISO 13616."""

import re

_MAX_LENGTH = 1000

# IBAN-Ländercodes mit der jeweils erlaubten Gesamtlänge (inkl. Ländercode und
# Prüfziffern) gemäß dem SWIFT-IBAN-Register. Ein Ländercode, der hier fehlt, ist für
# IBAN-Zwecke ungültig.
_IBAN_LENGTHS = {
    "AD": 24,
    "AE": 23,
    "AL": 28,
    "AT": 20,
    "AZ": 28,
    "BA": 20,
    "BE": 16,
    "BG": 22,
    "BH": 22,
    "BI": 27,
    "BR": 29,
    "BY": 28,
    "CH": 21,
    "CR": 22,
    "CY": 28,
    "CZ": 24,
    "DE": 22,
    "DJ": 27,
    "DK": 18,
    "DO": 28,
    "EE": 20,
    "EG": 29,
    "ES": 24,
    "FI": 18,
    "FO": 18,
    "FR": 27,
    "GB": 22,
    "GE": 22,
    "GI": 23,
    "GL": 18,
    "GR": 27,
    "GT": 28,
    "HR": 21,
    "HU": 28,
    "IE": 22,
    "IL": 23,
    "IQ": 23,
    "IS": 26,
    "IT": 27,
    "JO": 30,
    "KW": 30,
    "KZ": 20,
    "LB": 28,
    "LC": 32,
    "LI": 21,
    "LT": 20,
    "LU": 20,
    "LV": 21,
    "LY": 25,
    "MC": 27,
    "MD": 24,
    "ME": 22,
    "MK": 19,
    "MR": 27,
    "MT": 31,
    "MU": 30,
    "NL": 18,
    "NO": 15,
    "PK": 24,
    "PL": 28,
    "PS": 29,
    "PT": 25,
    "QA": 29,
    "RO": 24,
    "RS": 22,
    "RU": 33,
    "SA": 24,
    "SC": 31,
    "SE": 24,
    "SI": 19,
    "SK": 24,
    "SM": 27,
    "ST": 25,
    "SV": 28,
    "TL": 23,
    "TN": 24,
    "TR": 26,
    "UA": 29,
    "VA": 22,
    "VG": 24,
}

# Kein verschachtelter Quantor, kein Backtracking-Risiko: eine einzelne Zeichenklasse
# mit einem Quantor ist linear.
_IBAN_PATTERN = re.compile(r"[A-Z0-9]+")


def is_valid_iban(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError(f"expected a string, got {type(text).__name__}")
    if len(text) > _MAX_LENGTH:
        raise ValueError("input is too long (maximum 1000 characters)")

    compact = text.replace(" ", "")
    if not _IBAN_PATTERN.fullmatch(compact):
        raise ValueError("invalid characters (only A-Z and 0-9 are allowed)")

    country = compact[:2]
    if country not in _IBAN_LENGTHS:
        raise ValueError("invalid country code")

    if len(compact) != _IBAN_LENGTHS[country]:
        raise ValueError("invalid IBAN length")

    if not compact[2:4].isdigit():
        raise ValueError("invalid check digits")

    rearranged = compact[4:] + compact[:4]
    numeric = "".join(str(ord(ch) - 55) if "A" <= ch <= "Z" else ch for ch in rearranged)
    return int(numeric) % 97 == 1
