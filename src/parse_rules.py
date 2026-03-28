import json
import argparse
from pathlib import Path


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


def normalize_conditions(conditions):
    if not isinstance(conditions, list):
        conditions = []
    out = []
    for c in conditions:
        c = str(c).strip().lower().replace(" ", "_")
        if c:
            out.append(c)
    return sorted(set(out))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/responses_raw.jsonl")
    parser.add_argument("--output", default="data/rules_structured.jsonl")
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))
    rules = []

    for row in rows:
        scenario = row.get("scenario", {})
        parsed = row.get("parsed")
        error = row.get("error")

        if error or not parsed:
            continue

        judgment = str(parsed.get("judgment", "unknown")).strip().lower()
        action = str(parsed.get("action", "unknown")).strip().lower()
        conditions = normalize_conditions(parsed.get("conditions", []))
        principle = str(parsed.get("principle", "")).strip()
        confidence = parsed.get("confidence", 0.0)

        try:
            confidence = float(confidence)
        except Exception:
            confidence = 0.0

        rule = {
            "scenario_id": scenario.get("id"),
            "pair_id": scenario.get("pair_id"),
            "group_id": scenario.get("group_id"),
            "framing": scenario.get("framing"),
            "category": scenario.get("category"),
            "text": scenario.get("text"),
            "judgment": judgment,
            "action": action,
            "conditions": conditions,
            "principle": principle,
            "confidence": confidence,
            "rule_repr": f"{judgment}({action})",
        }

        rules.append(rule)

    write_jsonl(Path(args.output), rules)
    print(f"Wrote {len(rules)} structured rules to {args.output}")


if __name__ == "__main__":
    main()