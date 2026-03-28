import json
from pathlib import Path

TARGET_IDS = {"W01", "W02", "U01", "U02"}


def main():
    path = Path("data/responses_raw.jsonl")
    if not path.exists():
        print("responses_raw.jsonl not found")
        return

    kept = []
    removed = 0
    total = 0

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            row = json.loads(line)
            sid = (row.get("scenario") or {}).get("id")
            if sid in TARGET_IDS:
                removed += 1
                continue
            kept.append(row)

    with path.open("w", encoding="utf-8") as f:
        for row in kept:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Total before: {total}")
    print(f"Removed rows: {removed}")
    print(f"Total after:  {len(kept)}")


if __name__ == "__main__":
    main()
