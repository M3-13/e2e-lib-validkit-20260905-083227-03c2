"""Maskierung von Geheimnissen: alle Zeichen außer den letzten `keep` durch '*' ersetzen."""

_MAX_TEXT_LENGTH = 1000


def mask_secret(text: str, keep: int = 4) -> str:
    if not isinstance(text, str):
        raise TypeError("Text muss ein String sein")

    if len(text) > _MAX_TEXT_LENGTH:
        raise ValueError("Text überschreitet die maximale Länge")

    if not isinstance(keep, int) or isinstance(keep, bool):
        raise TypeError("keep muss eine ganze Zahl sein")

    if keep < 0:
        raise ValueError("keep darf nicht negativ sein")

    if keep >= len(text):
        return text

    return "*" * (len(text) - keep) + text[len(text) - keep :]
