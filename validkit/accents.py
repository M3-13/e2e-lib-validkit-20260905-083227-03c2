"""Entfernt diakritische Zeichen (Akzente) aus einem Text.

Die Funktion normalisiert den Text mit der Unicode-Normalform NFD und filtert
anschließend alle kombinierenden Zeichen heraus. Die Maximallänge wird vor der
Verarbeitung geprüft (AC-13); Fehlermeldungen nennen nur Typ und Form des
Fehlers, niemals Eingabewerte (AC-15).
"""

import unicodedata

MAX_TEXT_LENGTH = 1000


def strip_accents(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("strip_accents erwartet eine Zeichenkette (str).")

    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError("Der Text ist zu lang: maximal 1000 Zeichen sind zulässig.")

    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char))
