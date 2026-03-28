import subprocess
from pathlib import Path

FACTS = Path("asp_facts.lp")
RULES = Path("asp_rules.lp")
CLINGO = "clingo"  # ggf. Pfad anpassen


def run_clingo(facts=FACTS, rules=RULES, clingo_path=CLINGO):
    cmd = [clingo_path, str(facts), str(rules), "--outf=2"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Clingo-Fehler:", result.stderr)
        return None
    return result.stdout


def parse_contradictions(clingo_json):
    import json
    data = json.loads(clingo_json)
    contradictions = set()
    for call in data.get("Call", []):
        for witness in call.get("Witnesses", []):
            for value in witness.get("Value", []):
                if value.startswith("contradiction("):
                    # contradiction(Szenario,Aktion)
                    args = value[len("contradiction("):-1]
                    sid, action = [x.strip().strip('"') for x in args.split(",")[:2]]
                    contradictions.add((sid, action))
    return contradictions


def main():
    print("Starte Clingo-Konsistenzcheck...")
    output = run_clingo()
    if output is None:
        return
    contradictions = parse_contradictions(output)
    if contradictions:
        print(f"Gefundene Widersprüche ({len(contradictions)}):")
        for sid, action in sorted(contradictions):
            print(f"  - Szenario: {sid}, Aktion: {action}")
    else:
        print("Keine Widersprüche gefunden.")

if __name__ == "__main__":
    main()
