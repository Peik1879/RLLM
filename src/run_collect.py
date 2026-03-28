import os
import re
import json
import time
import argparse
from pathlib import Path

import requests
from dotenv import load_dotenv

from prompts import build_prompt


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


def append_jsonl(path: Path, item: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def extract_first_json_object(text: str):
    """
    Robust JSON extraction:
    1. Try direct json.loads
    2. Try extracting first {...} block
    """
    text = text.strip()

    # 1) direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # 2) extract first JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        candidate = match.group(0)
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None


def normalize_parsed_output(parsed: dict):
    """
    Make parsed result stable even if model output is imperfect.
    """
    if not isinstance(parsed, dict):
        return None

    judgment = str(parsed.get("judgment", "")).strip().lower()
    action = str(parsed.get("action", "")).strip().lower()
    conditions = parsed.get("conditions", [])
    principle = str(parsed.get("principle", "")).strip()
    confidence = parsed.get("confidence", 0.0)

    if judgment not in {"permitted", "forbidden", "obligatory"}:
        judgment = "unknown"

    if not action:
        action = "unknown"

    if not isinstance(conditions, list):
        conditions = [str(conditions)]

    normalized_conditions = []
    for c in conditions:
        c = str(c).strip().lower().replace(" ", "_")
        if c:
            normalized_conditions.append(c)

    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.0

    confidence = max(0.0, min(1.0, confidence))

    return {
        "judgment": judgment,
        "action": action,
        "conditions": normalized_conditions,
        "principle": principle,
        "confidence": confidence,
    }


def call_ollama(prompt: str, model: str, temperature: float = 0.2):
    """
    Calls local Ollama server.
    Default endpoint: http://localhost:11434/api/generate
    """
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": temperature
        }
    }

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    # Ollama usually returns generated text in 'response'
    return data.get("response", "").strip(), data


def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/scenarios.jsonl")
    parser.add_argument("--output", default="data/responses_raw.jsonl")
    parser.add_argument("--model", default="llama3")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    scenarios = load_jsonl(input_path)
    if args.limit is not None:
        scenarios = scenarios[:args.limit]

    processed_ids = set()
    if args.resume and output_path.exists():
        old_rows = load_jsonl(output_path)
        for row in old_rows:
            scenario = row.get("scenario", {})
            sid = scenario.get("id")
            if sid:
                processed_ids.add(sid)

    print(f"Loaded {len(scenarios)} scenarios.")
    if processed_ids:
        print(f"Resume mode: skipping {len(processed_ids)} already processed scenarios.")

    for idx, scenario in enumerate(scenarios, start=1):
        sid = scenario.get("id", f"unknown_{idx}")
        if sid in processed_ids:
            continue

        text = scenario.get("text", "").strip()
        if not text:
            print(f"[{idx}] Skipping empty scenario: {sid}")
            continue

        prompt = build_prompt(text)

        print(f"[{idx}/{len(scenarios)}] Processing scenario {sid} ...")

        raw_text = ""
        parsed = None
        error = None
        raw_meta = None

        try:
            raw_text, raw_meta = call_ollama(
                prompt=prompt,
                model=args.model,
                temperature=args.temperature
            )
            extracted = extract_first_json_object(raw_text)
            parsed = normalize_parsed_output(extracted)
            if parsed is None:
                error = "Failed to parse model output into valid normalized JSON."
        except Exception as e:
            error = str(e)

        row = {
            "scenario": scenario,
            "raw": raw_text,
            "parsed": parsed,
            "error": error,
            "model": args.model,
            "provider": "ollama",
            "timestamp": int(time.time()),
            "meta": raw_meta,
        }

        append_jsonl(output_path, row)

        if error:
            print(f"  -> ERROR: {error}")
        else:
            print(f"  -> OK: judgment={parsed['judgment']}, action={parsed['action']}")

        if args.sleep > 0:
            time.sleep(args.sleep)


if __name__ == "__main__":
    main()
