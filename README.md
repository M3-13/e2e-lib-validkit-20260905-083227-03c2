# validkit

`validkit` ist eine kleine, eigenständige Python-Bibliothek mit neun voneinander
unabhängigen, reinen Prüf- und Normalisierungsfunktionen. Jede Funktion ist
einzeln nutzbar, sauber typannotiert und meldet ungültige Eingaben mit einem
aussagekräftigen Fehler. Es gibt keine CLI, keine UI und keine Netzwerkzugriffe —
nur die Python-Standardbibliothek.

## Tech-Stack

- **Sprache:** Python 3 (≥ 3.10)
- **Tests:** pytest
- **Paketierung:** `pyproject.toml` (nur Standardbibliothek, keine externen Laufzeit-Abhängigkeiten)

## Installation

```bash
python -m pip install -e .
```

## Ausführung / Tests

Die Bibliothek besitzt keine eigene Anwendung. Sie wird importiert und aufgerufen:

```bash
python -c "import validkit"
```

Die Test-Suite läuft mit:

```bash
python -m pytest
```

## Fehlersemantik bei ungültigen Eingaben

- Falscher Typ (z. B. ein `int` statt eines `str`) führt zu einem `TypeError`.
- Ein ungültiger Wert oder ein ungültiges Format führt zu einem `ValueError`.
- Fehlermeldungen benennen ausschließlich Typ und Form des Fehlers — niemals die
  übergebenen Eingabewerte (insbesondere keine E-Mail-Adressen, Telefonnummern,
  IBANs oder Klartext-Geheimnisse).
- Alle Funktionen mit einem `str`-Parameter lehnen Eingaben mit mehr als 1000
  Zeichen mit einem `ValueError` ab, bevor die Verarbeitung beginnt.

## Funktionen und Beispiele

### `is_valid_email(text: str) -> bool`

Prüft, ob `text` eine syntaktisch gültige E-Mail-Adresse ist.

```python
from validkit import is_valid_email

is_valid_email("user@example.com")  # True
is_valid_email("user@")  # ValueError
```

### `luhn_check(digits: str | int) -> bool`

Prüft eine Ziffernfolge mit dem Luhn-Algorithmus.

```python
from validkit import luhn_check

luhn_check("79927398713")  # True
luhn_check("79927398712")  # False
```

### `is_valid_isbn13(text: str) -> bool`

Prüft eine ISBN-13 inklusive Prüfziffer.

```python
from validkit import is_valid_isbn13

is_valid_isbn13("978-3-16-148410-0")  # True
```

### `is_valid_iban(text: str) -> bool`

Prüft eine IBAN inklusive Länderkennung und Prüfziffer.

```python
from validkit import is_valid_iban

is_valid_iban("DE89 3704 0044 0532 0130 00")  # True
```

### `normalize_phone(text: str, country_code: str) -> str`

Normalisiert eine Telefonnummer auf das internationale Format `+<Ländercode><Rufnummer>`.

```python
from validkit import normalize_phone

normalize_phone("030 1234567", "49")  # '+49301234567'
normalize_phone("0049 170 1234567", "49")  # '+491701234567'
```

### `strip_accents(text: str) -> str`

Entfernt diakritische Zeichen.

```python
from validkit import strip_accents

strip_accents("München")  # 'Munchen'
strip_accents("café")  # 'cafe'
```

### `mask_secret(text: str, keep: int = 4) -> str`

Maskiert ein Geheimnis und lässt die letzten `keep` Zeichen sichtbar.

```python
from validkit import mask_secret

mask_secret("geheim", keep=2)  # '****im'
mask_secret("abc")  # 'abc'
```

### `slugify(text: str) -> str`

Erzeugt einen URL-fähigen Slug.

```python
from validkit import slugify

slugify("Héllo Wörld!")  # 'hello-world'
```

### `clamp(value: int | float, low: int | float, high: int | float) -> int | float`

Begrenzt `value` auf das Intervall `[low, high]`.

```python
from validkit import clamp

clamp(5, 0, 10)  # 5
clamp(-5, 0, 10)  # 0
clamp(15, 0, 10)  # 10
```

## Funktionsübersicht

| Funktion | Modul | Aufgabe |
| --- | --- | --- |
| `is_valid_email` | `validkit.email` | E-Mail-Adressen prüfen |
| `luhn_check` | `validkit.luhn` | Luhn-Prüfsumme |
| `is_valid_isbn13` | `validkit.isbn` | ISBN-13 prüfen |
| `is_valid_iban` | `validkit.iban` | IBAN prüfen |
| `normalize_phone` | `validkit.phone` | Telefonnummern normalisieren |
| `strip_accents` | `validkit.accents` | Diakritika entfernen |
| `mask_secret` | `validkit.mask` | Geheimnisse maskieren |
| `slugify` | `validkit.slug` | URL-Slugs erzeugen |
| `clamp` | `validkit.clamp` | Werte begrenzen |
