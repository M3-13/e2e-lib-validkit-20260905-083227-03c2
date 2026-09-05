"""Telefonnummern-Normalisierung."""

_MAX_LENGTH = 1000
_SEPARATORS = str.maketrans("", "", " ()-.")


def normalize_phone(text: str, country_code: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text muss eine Zeichenkette (str) sein")
    if not isinstance(country_code, str):
        raise TypeError("country_code muss eine Zeichenkette (str) sein")
    if len(text) > _MAX_LENGTH:
        raise ValueError("text überschreitet die Maximallänge von 1000 Zeichen")
    if len(country_code) > _MAX_LENGTH:
        raise ValueError("country_code überschreitet die Maximallänge von 1000 Zeichen")

    prefix = country_code
    if prefix.startswith("+"):
        prefix = prefix[1:]
    if not prefix or not (prefix.isascii() and prefix.isdigit()):
        raise ValueError("country_code muss eine Ziffernfolge sein")

    number = text.translate(_SEPARATORS)

    international = False
    if number.startswith("+"):
        number = number[1:]
        international = True
    elif number.startswith("00"):
        number = number[2:]
        international = True

    if not number:
        raise ValueError("Telefonnummer hat keinen nationalen Teil")
    if not (number.isascii() and number.isdigit()):
        raise ValueError("Telefonnummer enthält ungültige Zeichen")

    if international:
        return "+" + number

    if number.startswith("0"):
        number = number[1:]
        if not number:
            raise ValueError("Telefonnummer hat keinen nationalen Teil")

    return "+" + prefix + number
