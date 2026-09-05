"""Syntaktische E-Mail-Validierung ohne Netzwerkzugriff."""

import re

_MAX_LENGTH = 1000

# Lokaler Teil: atext-Zeichen (RFC 5322), Punkt nur als Trenner zwischen Atomen,
# daher keine führenden/abschließenden oder aufeinanderfolgenden Punkte möglich.
_ATEXT = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]"
_LOCAL_PART = _ATEXT + r"+(?:\." + _ATEXT + r"+)*"

# Domänen-Label: alphanumerisch, Bindestriche nur im Inneren.
_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"

# Domänenteil mit mindestens einem Punkt (mindestens zwei Labels).
_EMAIL_PATTERN = re.compile(
    _LOCAL_PART + r"@" + _LABEL + r"\." + _LABEL + r"(?:\." + _LABEL + r")*"
)


def is_valid_email(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError("is_valid_email erwartet einen String")
    if text == "":
        raise ValueError("E-Mail-Adresse darf nicht leer sein")
    if len(text) > _MAX_LENGTH:
        raise ValueError(
            f"E-Mail-Adresse überschreitet die maximale Länge von {_MAX_LENGTH} Zeichen"
        )
    return _EMAIL_PATTERN.fullmatch(text) is not None
