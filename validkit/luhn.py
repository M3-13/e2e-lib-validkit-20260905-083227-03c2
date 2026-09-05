def luhn_check(digits: str | int) -> bool:
    """Prüft eine Ziffernfolge inklusive Prüfziffer mit dem Luhn-Algorithmus.

    Die Ziffernfolge kann als `str` oder als nicht-negatives `int` übergeben
    werden. Gültige Folgen ergeben `True`, ungültige `False`. Nicht-Ziffern,
    leere Folgen und Folgen mit weniger als zwei Ziffern werfen einen
    `ValueError`, ein falscher Typ einen `TypeError`. Fehlermeldungen enthalten
    keine Eingabewerte.
    """
    if isinstance(digits, bool):
        raise TypeError("digits must be a string or an integer")
    if isinstance(digits, int):
        if digits < 0:
            raise ValueError("digits must be a non-negative integer")
        digits = str(digits)
    elif isinstance(digits, str):
        if len(digits) > 1000:
            raise ValueError("digits must not exceed 1000 characters")
    else:
        raise TypeError("digits must be a string or an integer")

    if len(digits) < 2:
        raise ValueError("digits must contain at least two digits")
    if not (digits.isascii() and digits.isdigit()):
        raise ValueError("digits must contain only digits")

    total = 0
    for index, char in enumerate(reversed(digits)):
        value = int(char)
        if index % 2 == 1:
            value *= 2
            if value > 9:
                value -= 9
        total += value

    return total % 10 == 0
