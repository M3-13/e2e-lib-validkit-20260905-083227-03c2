VERDICT: CHANGES_REQUESTED

## Sicherheitsbericht

### Scanner-Abdeckung
`bandit` und `semgrep` wurden übersprungen (`[skipped]`). Das wird als Analyselücke notiert, stellt aber selbst keinen Befund dar. Die folgende Bewertung basiert auf manueller Quellcodeanalyse.

### Befund 1: Fehlende Längenbegrenzung für `int`-Eingaben in `luhn_check`
- **Schweregrad:** low – Härtung, kein unmittelbar remote ausnutzbarer Angriff
- **Datei/Stelle:** `validkit/luhn.py`, `if isinstance(digits, int):`-Zweig
- **Problem:**  
  Bei `str`-Eingaben wird die Maximallänge von 1000 Zeichen geprüft. Bei `int`-Eingaben wird die Zahl dagegen ohne eigene Längenprüfung per `digits = str(digits)` konvertiert und anschließend zeichenweise verarbeitet. Sehr große Ganzzahlen können dadurch unverhältnismäßig viel CPU/Speicher binden. In neueren Python-Versionen kann die Konvertierung großer Integer in Strings zudem eine interpreterabhängige `ValueError` auslösen, die nicht von der Bibliothek kontrolliert wird. Damit ist der `int`-Pfad nicht durch die in AC-13 geforderte Maximallängenprüfung abgedeckt.
- **Konkreter Fix:**  
  Eine einheitliche Grenze vor der ressourcenintensiven Verarbeitung setzen, z. B.:
  ```python
  _MAX_DIGITS = 1000

  if isinstance(digits, int):
      if digits < 0:
          raise ValueError("digits must be a non-negative integer")
      if digits >= 10 ** _MAX_DIGITS:
          raise ValueError("digits must not exceed 1000 digits")
      digits = str(digits)
  ```
  Alternativ nach der Konvertierung `len(digits) > 1000` prüfen, sofern die Konvertierung selbst keine interpreterabhängige Grenze sprengt.

### Weitere Prüfpunkte
- **Geheimnisse:** Keine hartkodierten Schlüssel, Passwörter, Token oder URLs sichtbar.
- **Injection/ReDoS:** Die eingesetzten regulären Ausdrücke (`email`, `iban`, `slugify`) sind deterministisch; Längenlimits greifen vor der Regex-Ausführung. Kein katastrophales Backtracking erkennbar.
- **AuthN/AuthZ:** Nicht vorhanden; reine Bibliothek ohne Netzwerk-/Session-Logik.
- **Abhängigkeiten:** `pyproject.toml` deklariert keine Laufzeitabhängigkeiten; nur `pytest` als optionale Dev-Abhängigkeit. Keine bekannte verwundbare Dependency sichtbar.
- **Datenschutz/Fehlermeldungen:** Die geprüften Fehlermeldungen enthalten keine übergebenen Eingabewerte, sondern benennen Typ und Form des Fehlers. Tests bestätigen dies weitgehend.
- **Transport/Konfiguration:** Keine Netzwerkfunktionalität, keine unsicheren Defaults oder Debug-/CORS-Einstellungen sichtbar.

### Fazit
Es wurde keine kritische oder hohe Schwachstelle festgestellt. Aufgrund der fehlenden Längenprüfung im `int`-Pfad von `luhn_check` wird eine Härtung empfohlen; daher `CHANGES_REQUESTED`.