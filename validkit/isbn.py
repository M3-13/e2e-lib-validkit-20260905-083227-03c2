"""ISBN-13-Prüfung."""

_MAX_LENGTH = 1000


def is_valid_isbn13(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError("is_valid_isbn13 expects a str")
    if len(text) > _MAX_LENGTH:
        raise ValueError("input exceeds maximum allowed length of 1000 characters")

    digits = text.replace("-", "").replace(" ", "")
    if not digits:
        raise ValueError("ISBN-13 must not be empty")
    if any(c < "0" or c > "9" for c in digits):
        raise ValueError("ISBN-13 may only contain digits, hyphens and spaces")
    if len(digits) != 13:
        raise ValueError("ISBN-13 must contain exactly 13 digits")

    total = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(digits))
    return total % 10 == 0
