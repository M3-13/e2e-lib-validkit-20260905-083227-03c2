"""URL-Slug-Erzeugung: wandelt Text in einen URL-tauglichen Slug um."""

import re
import unicodedata

_MAX_LENGTH = 1000

_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("slugify erwartet einen String als Eingabe.")
    if len(text) > _MAX_LENGTH:
        raise ValueError("Eingabe darf höchstens 1000 Zeichen lang sein.")
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = _NON_ALNUM_RE.sub("-", ascii_text.lower()).strip("-")
    if not slug:
        raise ValueError("Eingabe ergibt nach Normalisierung keinen gültigen Slug.")
    return slug
