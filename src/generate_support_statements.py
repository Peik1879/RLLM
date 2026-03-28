import argparse
import time
from pathlib import Path

from reasoning_pipeline_utils import (
    append_jsonl,
    call_ollama,
    extract_first_json_object,
    load_jsonl,
)


PROMPT_TEMPLATE = """
You are a careful moral reasoner.

Given one normative atom and context, produce ONE short supporting statement.
The statement must support the atom directly and must not switch stance.

Return JSON only:
{{
  "support_statement": "1-2 sentence supporting statement",
  "support_type": "principle|consequence|duty|rights|authority",
  "alignment": "supports",
  "confidence": 0.0
}}

Normative atom: {atom}
Action: {action}
Judgment: {judgment}
Conditions: {conditions}
Source principle: {principle}
Scenario text: {text}
""".strip()


def normalize_support(parsed: dict):
    if not isinstance(parsed, dict):
        return None

    statement = str(parsed.get("support_statement", "")).strip()
    support_type = str(parsed.get("support_type", "principle")).strip().lower()
    alignment = str(parsed.get("alignment", "")).strip().lower()
    confidence = parsed.get("confidence", 0.0)

    if not statement:
        return None

    if support_type not in {"principle", "consequence", "duty", "rights", "authority"}:
        support_type = "principle"

    if alignment != "supports":
        alignment = "supports"

    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))

    return {
        "support_statement": statement,
        "support_type": support_type,
        "alignment": alignment,
        "confidence": confidence,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/moral_atoms.jsonl")
    parser.add_argument("--output", default="data/support_statements.jsonl")
    parser.add_argument("--model", default="llama3:latest")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    atoms = load_jsonl(Path(args.input))
    if args.limit is not None:
        atoms = atoms[: args.limit]

    processed_ids = set()
    out_path = Path(args.output)
    if args.resume and out_path.exists():
        old = load_jsonl(out_path)
        for row in old:
            sid = row.get("scenario_id")
            if sid:
                processed_ids.add(sid)

    print(f"Loaded {len(atoms)} atoms.")
    if processed_ids:
        print(f"Resume mode: skipping {len(processed_ids)} already processed rows.")

    for idx, atom in enumerate(atoms, start=1):
        sid = atom.get("scenario_id", f"unknown_{idx}")
        if sid in processed_ids:
            continue

        prompt = PROMPT_TEMPLATE.format(
            atom=atom.get("atom", ""),
            action=atom.get("action", ""),
            judgment=atom.get("judgment", ""),
            conditions=", ".join(atom.get("conditions", [])),
            principle=atom.get("principle", ""),
            text=atom.get("text", ""),
        )

        print(f"[{idx}/{len(atoms)}] Generating support for {sid} ...")

        raw = ""
        parsed = None
        error = None
        meta = None

        try:
            raw, meta = call_ollama(
                prompt=prompt,
                model=args.model,
                temperature=args.temperature,
            )
            extracted = extract_first_json_object(raw)
            parsed = normalize_support(extracted)
            if parsed is None:
                error = "Failed to parse support JSON"
        except Exception as exc:
            error = str(exc)

        row = {
            "scenario_id": sid,
            "group_id": atom.get("group_id"),
            "framing": atom.get("framing"),
            "category": atom.get("category"),
            "atom": atom.get("atom"),
            "judgment": atom.get("judgment"),
            "action": atom.get("action"),
            "conditions": atom.get("conditions", []),
            "source_principle": atom.get("principle"),
            "support": parsed,
            "raw": raw,
            "error": error,
            "model": args.model,
            "timestamp": int(time.time()),
            "meta": meta,
        }
        append_jsonl(out_path, row)

        if error:
            print(f"  -> ERROR: {error}")
        else:
            print(f"  -> OK: type={parsed['support_type']} conf={parsed['confidence']:.2f}")

        if args.sleep > 0:
            time.sleep(args.sleep)


if __name__ == "__main__":
    main()
