import json
from pathlib import Path

# Konfiguration
INPUT = Path("data/responses_raw.jsonl")
OUTPUT = Path("asp_facts.lp")

# Hilfsfunktion für ASP-Fakten

def asp_facts_from_entry(entry):
    facts = []
    sid = entry["scenario"]["id"]
    parsed = entry["parsed"]
    judgment = parsed["judgment"].lower()
    action = parsed["action"].lower()
    # Jede Bedingung als separates Faktum
    for cond in parsed["conditions"]:
        facts.append(f"judgment(\"{sid}\",{judgment},{action},\"{cond}\").")
    return facts

# Hauptfunktion

def main():
    with INPUT.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    all_facts = []
    for line in lines:
        if not line.strip():
            continue
        entry = json.loads(line)
        if "parsed" not in entry or not entry["parsed"]:
            continue
        all_facts.extend(asp_facts_from_entry(entry))
    with OUTPUT.open("w", encoding="utf-8") as f:
        for fact in all_facts:
            f.write(fact + "\n")
    print(f"{len(all_facts)} ASP-Fakten nach {OUTPUT} exportiert.")

if __name__ == "__main__":
    main()
