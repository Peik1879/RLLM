import json
import argparse
from pathlib import Path
from itertools import combinations


CONTRADICTORY_PAIRS = {
    ("permitted", "forbidden"),
    ("forbidden", "permitted"),
    ("obligatory", "forbidden"),
    ("forbidden", "obligatory"),
}

CONSISTENT_JUDGMENT_PAIRS = {
    ("obligatory", "forbidden"),
    ("forbidden", "obligatory"),
    ("permitted", "permitted"),
}


def load_jsonl(path: Path):
    items = []
    if not path.exists():
        return items
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def write_jsonl(path: Path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def jaccard(a, b):
    a = set(a or [])
    b = set(b or [])
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def is_contradiction(rule1, rule2):
    j1 = rule1["judgment"]
    j2 = rule2["judgment"]
    a1 = rule1["action"]
    a2 = rule2["action"]

    if a1 != a2:
        return False

    return (j1, j2) in CONTRADICTORY_PAIRS


def contradiction_strength(rule1, rule2, condition_threshold=0.5):
    same_pair = (
        rule1.get("pair_id") is not None and
        rule1.get("pair_id") == rule2.get("pair_id")
    )

    same_category = (
        rule1.get("category") is not None and
        rule1.get("category") == rule2.get("category")
    )

    sim = jaccard(rule1.get("conditions", []), rule2.get("conditions", []))

    if same_pair:
        return "strong", sim
    if sim >= condition_threshold:
        return "moderate", sim
    if same_category:
        return "weak", sim
    return "very_weak", sim


def pair_contradiction_type(j1, j2):
    if j1 == "obligatory" and j2 == "obligatory":
        return "double_obligatory_paradox"
    if j1 == "forbidden" and j2 == "forbidden":
        return "double_forbidden_paradox"
    if {j1, j2} == {"obligatory", "permitted"}:
        return "obligation_permission_conflict"
    if {j1, j2} == {"forbidden", "permitted"}:
        return "permission_prohibition_conflict"
    if {j1, j2} == {"obligatory", "forbidden"}:
        return "inverse_obligation_forbidden_consistent"
    if j1 == "permitted" and j2 == "permitted":
        return "dual_permission_consistent"
    return "unknown"


def is_pair_semantically_contradictory(rule1, rule2):
    j1 = rule1.get("judgment")
    j2 = rule2.get("judgment")
    return (j1, j2) not in CONSISTENT_JUDGMENT_PAIRS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/rules_structured.jsonl")
    parser.add_argument("--output", default="data/contradictions.jsonl")
    parser.add_argument("--condition-threshold", type=float, default=0.5)
    parser.add_argument(
        "--mode",
        choices=["semantic_pairs", "technical_action_match", "framing_groups"],
        default="semantic_pairs",
        help=(
            "semantic_pairs: compare inverse scenario pairs by judgment logic; "
            "technical_action_match: only compare exact same action labels; "
            "framing_groups: check judgment consistency across framings within each group"
        ),
    )
    args = parser.parse_args()

    rules = load_jsonl(Path(args.input))
    contradictions = []

    if args.mode == "framing_groups":
        by_group = {}
        for rule in rules:
            gid = rule.get("group_id")
            if gid:
                by_group.setdefault(gid, []).append(rule)

        for group_id in sorted(by_group.keys()):
            group_rules = by_group[group_id]
            framing_judgments = {
                r.get("framing", "unknown"): r.get("judgment") for r in group_rules
            }
            unique_judgments = set(framing_judgments.values())
            is_consistent = len(unique_judgments) <= 1

            if not is_consistent:
                contradictions.append({
                    "type": "framing_inconsistency",
                    "group_id": group_id,
                    "category": group_rules[0].get("category"),
                    "framing_judgments": framing_judgments,
                    "unique_judgment_count": len(unique_judgments),
                    "scenario_ids": [r.get("scenario_id") for r in group_rules],
                })

    elif args.mode == "technical_action_match":
        for r1, r2 in combinations(rules, 2):
            if not is_contradiction(r1, r2):
                continue

            strength, similarity = contradiction_strength(
                r1, r2, condition_threshold=args.condition_threshold
            )

            contradiction = {
                "type": "judgment_conflict",
                "action": r1["action"],
                "rule_1": {
                    "scenario_id": r1.get("scenario_id"),
                    "pair_id": r1.get("pair_id"),
                    "category": r1.get("category"),
                    "judgment": r1.get("judgment"),
                    "conditions": r1.get("conditions"),
                    "principle": r1.get("principle"),
                    "rule_repr": r1.get("rule_repr"),
                },
                "rule_2": {
                    "scenario_id": r2.get("scenario_id"),
                    "pair_id": r2.get("pair_id"),
                    "category": r2.get("category"),
                    "judgment": r2.get("judgment"),
                    "conditions": r2.get("conditions"),
                    "principle": r2.get("principle"),
                    "rule_repr": r2.get("rule_repr"),
                },
                "condition_similarity": similarity,
                "strength": strength,
            }

            contradictions.append(contradiction)
    else:
        by_pair = {}
        for rule in rules:
            pid = rule.get("pair_id")
            if not pid:
                continue
            by_pair.setdefault(pid, []).append(rule)

        for pair_id, pair_rules in sorted(by_pair.items()):
            if len(pair_rules) != 2:
                continue

            r1, r2 = sorted(pair_rules, key=lambda x: str(x.get("scenario_id", "")))
            j1 = r1.get("judgment")
            j2 = r2.get("judgment")

            if not is_pair_semantically_contradictory(r1, r2):
                continue

            contradiction = {
                "type": "semantic_pair_conflict",
                "pair_id": pair_id,
                "category": r1.get("category") or r2.get("category"),
                "judgment_pair": [j1, j2],
                "conflict_type": pair_contradiction_type(j1, j2),
                "rule_1": {
                    "scenario_id": r1.get("scenario_id"),
                    "judgment": j1,
                    "action": r1.get("action"),
                    "confidence": r1.get("confidence"),
                    "principle": r1.get("principle"),
                },
                "rule_2": {
                    "scenario_id": r2.get("scenario_id"),
                    "judgment": j2,
                    "action": r2.get("action"),
                    "confidence": r2.get("confidence"),
                    "principle": r2.get("principle"),
                },
            }

            contradictions.append(contradiction)

    write_jsonl(Path(args.output), contradictions)

    print(f"Loaded {len(rules)} rules.")
    print(f"Mode: {args.mode}")
    print(f"Found {len(contradictions)} contradictions.")
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()