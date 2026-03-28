# Symbolic Consistency Checker for Moral Judgments

Ein transparentes, regelbasiertes System zur Überprüfung der logischen Konsistenz und Priorisierung moralischer Urteile mit erklärbarer Entscheidungsfindung.

## Features
- **Regelbasiertes Backend:** Alle moralischen Regeln und Fakten werden in ASP (Clingo) modelliert.
- **Kontext- und Prioritätensystem:** Konflikte werden durch ethisch gewichtete Prioritäten gelöst.
- **Erklärbarkeit:** Jede Entscheidung ist nachvollziehbar und wird mit Begründung ausgegeben.
- **Statistik:** Auswertung, welche Werte am häufigsten Konflikte entscheiden ("moralische Sieger").
- **Tkinter-GUI:** Einfache Bedienung, Anzeige von Konflikten, Erklärungen und Statistiken.
- **Modular:** Leicht erweiterbar um neue Regeln, Kontexte und Szenarien.

## Projektstruktur
- `facts.lp` — Szenarien, Urteile, Kontexte und Prioritäten (ASP-Fakten)
- `rules.lp` — Logik und Regeln für Konsistenz, Prioritäten, Erklärungen (ASP)
- `main.py` — Kommandozeilen-Tool für Konsistenzprüfung und Statistik
- `gui.py` — Tkinter-GUI für interaktive Nutzung
- `clingo_runner.py` — Schnittstelle zwischen Python und Clingo
- `parser.py` — Auswertung und Aufbereitung der Clingo-Ausgabe

## Voraussetzungen
- Python 3.8+
- Clingo (https://potassco.org/clingo/)
- Tkinter (in Standard-Python enthalten)

## Installation
1. Clingo installieren (siehe https://potassco.org/clingo/)
2. Projektdateien in ein Verzeichnis kopieren
3. Optional: Virtuelle Python-Umgebung anlegen

## Nutzung
### GUI starten
```bash
python gui.py
```

### Konsolenmodus
```bash
python main.py
```

## Beispiel-Auswertung
- Das System entscheidet 210 moralische Konflikte.
- 203 Konflikte werden durch Prioritäten gelöst.
- Die häufigsten "Sieger" sind: Nachhaltigkeit, Menschlichkeit, öffentliche Gesundheit.

## Anpassung & Erweiterung
- Neue Szenarien: In `facts.lp` ergänzen
- Neue Regeln: In `rules.lp` ergänzen
- Prioritäten anpassen: In `facts.lp` pro Kontext ändern

## Lizenz
MIT License

---

**Kontakt:** Für Fragen oder Anregungen: [Dein Name oder Kontakt]
