import argparse
from pathlib import Path

from reasoning_pipeline_utils import load_jsonl, write_jsonl


VALID_JUDGMENTS = {"permitted", "forbidden", "obligatory"}


def normalize_conditions(conditions):
    if not isinstance(conditions, list):
        return []
    out = []
    for c in conditions:
        c = str(c).strip().lower().replace(" ", "_")
        if c:
            out.append(c)
    return sorted(set(out))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/responses_raw.jsonl")
    parser.add_argument("--output", default="data/moral_atoms.jsonl")
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))
    atoms = []

    for row in rows:
        scenario = row.get("scenario", {})
        parsed = row.get("parsed") or {}
        error = row.get("error")

        if error:
            continue

        judgment = str(parsed.get("judgment", "unknown")).strip().lower()
        if judgment not in VALID_JUDGMENTS:
            continue

        action = str(parsed.get("action", "unknown")).strip().lower()
        if not action:
            action = "unknown"

        principle = str(parsed.get("principle", "")).strip()
        conditions = normalize_conditions(parsed.get("conditions", []))
        confidence = parsed.get("confidence", 0.0)

        try:
            confidence = float(confidence)
        except Exception:
            confidence = 0.0

        atom = {
            "scenario_id": scenario.get("id"),
            "group_id": scenario.get("group_id"),
            "framing": scenario.get("framing"),
            "category": scenario.get("category"),
            "text": scenario.get("text"),
            "judgment": judgment,
            "action": action,
            "conditions": conditions,
            "principle": principle,
            "confidence": confidence,
            "atom": f"{judgment}({action})",
        }
        atoms.append(atom)

    write_jsonl(Path(args.output), atoms)
    print(f"Wrote {len(atoms)} moral atoms to {args.output}")


if __name__ == "__main__":
    main()
