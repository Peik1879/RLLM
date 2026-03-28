from clingo_runner import run_clingo
from parser import parse_clingo_output

def main():
    facts_path = "facts.lp"
    rules_path = "rules.lp"
    output = run_clingo(facts_path, rules_path)
    result = parse_clingo_output(output)
    contradictions = result["contradictions"]
    explanations = result["explanations"]

    # 1. Zähle, wie oft Konflikte durch Prioritäten aufgelöst werden
    # 2. Zeige für jede Aktion, welcher Kontext am häufigsten gewinnt
    # Dazu: facts.lp einlesen und Prioritäten + Kontexte extrahieren
    from collections import defaultdict
    import re

    # Prioritäten extrahieren
    priorities = {}
    with open(facts_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"priority\\(([^,]+),\\s*(\\d+)\\)", line)
            if m:
                priorities[m.group(1)] = int(m.group(2))

    # Kontext pro Szenario/Aktion
    judgments = []
    with open(facts_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"judgment\\((\\d+),\\s*([^,]+),\\s*([^,]+),\\s*([^\)]+)\\)", line)
            if m:
                judgments.append({
                    "scenario": m.group(1),
                    "action": m.group(2),
                    "value": m.group(3),
                    "context": m.group(4)
                })

    # Für jede Aktion/Szenario: Wer "gewinnt"?
    win_stats = defaultdict(int)
    resolved_by_priority = 0
    total_conflicts = 0

    # Finde alle Konflikte (allow/forbid für selbe Aktion/Szenario)
    for j in judgments:
        if j["value"] == "allow":
            for k in judgments:
                if (
                    k["scenario"] == j["scenario"] and
                    k["action"] == j["action"] and
                    k["value"] == "forbid"
                ):
                    total_conflicts += 1
                    # Wer hat höhere Priorität?
                    p_allow = priorities.get(j["context"], 0)
                    p_forbid = priorities.get(k["context"], 0)
                    if p_allow > p_forbid:
                        win_stats[j["context"]] += 1
                        resolved_by_priority += 1
                    elif p_forbid > p_allow:
                        win_stats[k["context"]] += 1
                        resolved_by_priority += 1

    print("\n--- Statistik: Konfliktauflösung durch Prioritäten ---")
    print(f"Gesamtzahl Konflikte: {total_conflicts}")
    print(f"Davon durch Prioritäten aufgelöst: {resolved_by_priority}")
    print("\nKontext | Konflikte entschieden")
    print("------------------------------")
    for ctx, count in sorted(win_stats.items(), key=lambda x: -x[1]):
        print(f"{ctx:20} | {count}")

    print("\n| Scenario | Action | Status        |")
    print("| -------- | ------ | ------------- |")
    for c in contradictions:
        print(f"| {c['scenario']}        | {c['action']}  | {c['status']} |")
    if explanations:
        print("\nExplanations:")
        for e in explanations:
            print(f"Scenario {e['scenario']}, Action {e['action']}: {e['type']}")

if __name__ == "__main__":
    main()
