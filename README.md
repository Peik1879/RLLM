# Symbolic Consistency Checker for Moral Judgments

A transparent, rule-based system for checking the logical consistency and prioritization of moral judgments with explainable decision-making.

## Features
- **Rule-based backend:** All moral rules and facts are modeled in ASP (Clingo).
- **Context and priority system:** Conflicts are resolved using ethically weighted priorities.
- **Explainability:** Every decision is traceable and comes with an explanation.
- **Statistics:** Analysis of which values most frequently decide conflicts ("moral winners").
- **Tkinter GUI:** Easy-to-use interface, displays conflicts, explanations, and statistics.
- **Modular:** Easily extendable with new rules, contexts, and scenarios.

## Project Structure
- `facts.lp` — Scenarios, judgments, contexts, and priorities (ASP facts)
- `rules.lp` — Logic and rules for consistency, priorities, explanations (ASP)
- `main.py` — Command-line tool for consistency checking and statistics
- `gui.py` — Tkinter GUI for interactive use
- `clingo_runner.py` — Interface between Python and Clingo
- `parser.py` — Processing and formatting of Clingo output

## Requirements
- Python 3.8+
- Clingo (https://potassco.org/clingo/)
- Tkinter (included in standard Python)

## Installation
1. Install Clingo (see https://potassco.org/clingo/)
2. Copy project files into a directory
3. Optionally: Create a virtual Python environment

## Usage
### Start GUI
```bash
python gui.py
```

### Command-line mode
```bash
python main.py
```

## Example Evaluation
- The system resolves 210 moral conflicts.
- 203 conflicts are resolved by priorities.
- The most frequent "winners" are: sustainability, humanity, public health.

## Customization & Extension
- New scenarios: Add to `facts.lp`
- New rules: Add to `rules.lp`
- Adjust priorities: Change per context in `facts.lp`

## License
MIT License

---

**Contact:** For questions or suggestions: [Your Name or Contact]
