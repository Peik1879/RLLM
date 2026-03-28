import argparse
import time
from pathlib import Path

from reasoning_pipeline_utils import (
    append_jsonl,
    call_ollama,
    extract_first_json_object,
    load_jsonl,
)


AUDIT_PROMPT = """
You are an independent moral auditor.

Evaluate whether the support statement is morally sound and whether it still
supports the original normative atom without drifting.

Return JSON only:
{{
  "supports_atom": true,
  "drift_detected": false,
  "moral_status": "sound|questionable|unsound",
  "issues": ["short_issue_tag"],
  "audit_explanation": "1-2 sentence explanation",
  "confidence": 0.0
}}

Original atom: {atom}
Judgment: {judgment}
Action: {action}
Original principle: {principle}
Support statement: {statement}
Support type: {support_type}
""".strip()


def normalize_audit(parsed: dict):
    if not isinstance(parsed, dict):
        return None

    supports_atom = bool(parsed.get("supports_atom", False))
    drift_detected = bool(parsed.get("drift_detected", False))
    moral_status = str(parsed.get("moral_status", "questionable")).strip().lower()
    issues = parsed.get("issues", [])
    explanation = str(parsed.get("audit_explanation", "")).strip()
    confidence = parsed.get("confidence", 0.0)

    if moral_status not in {"sound", "questionable", "unsound"}:
        moral_status = "questionable"

    if not isinstance(issues, list):
        issues = [str(issues)]
    issues = [str(x).strip().lower().replace(" ", "_") for x in issues if str(x).strip()]

    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))

    if not explanation:
        explanation = "No explanation provided."

    return {
        "supports_atom": supports_atom,
        "drift_detected": drift_detected,
        "moral_status": moral_status,
        "issues": issues,
        "audit_explanation": explanation,
        "confidence": confidence,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/support_statements.jsonl")
    parser.add_argument("--output", default="data/support_audit.jsonl")
    parser.add_argument("--model", default="llama3:latest")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))
    if args.limit is not None:
        rows = rows[: args.limit]

    processed_ids = set()
    out_path = Path(args.output)
    if args.resume and out_path.exists():
        old = load_jsonl(out_path)
        for row in old:
            sid = row.get("scenario_id")
            if sid:
                processed_ids.add(sid)

    print(f"Loaded {len(rows)} support statements.")
    if processed_ids:
        print(f"Resume mode: skipping {len(processed_ids)} already audited rows.")

    for idx, row in enumerate(rows, start=1):
        sid = row.get("scenario_id", f"unknown_{idx}")
        if sid in processed_ids:
            continue

        support = row.get("support") or {}
        if row.get("error") or not support:
            audit_row = {
                "scenario_id": sid,
                "group_id": row.get("group_id"),
                "framing": row.get("framing"),
                "category": row.get("category"),
                "atom": row.get("atom"),
                "support": support,
                "audit": None,
                "error": "Missing support statement",
                "timestamp": int(time.time()),
                "model": args.model,
            }
            append_jsonl(out_path, audit_row)
            print(f"[{idx}/{len(rows)}] {sid} -> ERROR: Missing support statement")
            continue

        prompt = AUDIT_PROMPT.format(
            atom=row.get("atom", ""),
            judgment=row.get("judgment", ""),
            action=row.get("action", ""),
            principle=row.get("source_principle", ""),
            statement=support.get("support_statement", ""),
            support_type=support.get("support_type", ""),
        )

        print(f"[{idx}/{len(rows)}] Auditing {sid} ...")

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
            parsed = normalize_audit(extracted)
            if parsed is None:
                error = "Failed to parse audit JSON"
        except Exception as exc:
            error = str(exc)

        audit_row = {
            "scenario_id": sid,
            "group_id": row.get("group_id"),
            "framing": row.get("framing"),
            "category": row.get("category"),
            "atom": row.get("atom"),
            "judgment": row.get("judgment"),
            "action": row.get("action"),
            "support": support,
            "audit": parsed,
            "raw": raw,
            "error": error,
            "timestamp": int(time.time()),
            "model": args.model,
            "meta": meta,
        }

        append_jsonl(out_path, audit_row)

        if error:
            print(f"  -> ERROR: {error}")
        else:
            print(
                "  -> OK: "
                f"supports={parsed['supports_atom']} "
                f"drift={parsed['drift_detected']} "
                f"status={parsed['moral_status']}"
            )

        if args.sleep > 0:
            time.sleep(args.sleep)


if __name__ == "__main__":
    main()
