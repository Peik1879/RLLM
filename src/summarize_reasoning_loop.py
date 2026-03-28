import argparse
import csv
from collections import Counter
from pathlib import Path

from reasoning_pipeline_utils import load_jsonl


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/support_audit.jsonl")
    parser.add_argument("--summary-csv", default="reasoning_loop_summary.csv")
    parser.add_argument("--groups-csv", default="reasoning_loop_groups.csv")
    parser.add_argument("--summary-txt", default="reasoning_loop_summary.txt")
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))
    ok_rows = [r for r in rows if not r.get("error") and r.get("audit")]

    total = len(rows)
    ok = len(ok_rows)

    supports_true = sum(1 for r in ok_rows if r["audit"].get("supports_atom") is True)
    drift_true = sum(1 for r in ok_rows if r["audit"].get("drift_detected") is True)

    status_counter = Counter(r["audit"].get("moral_status", "unknown") for r in ok_rows)
    issues_counter = Counter()
    for r in ok_rows:
        for issue in r["audit"].get("issues", []):
            issues_counter[issue] += 1

    summary_rows = [
        {"metric": "total_rows", "value": total},
        {"metric": "audited_rows", "value": ok},
        {"metric": "supports_atom_true", "value": supports_true},
        {"metric": "drift_detected_true", "value": drift_true},
        {
            "metric": "supports_rate",
            "value": f"{(supports_true / ok * 100.0):.1f}%" if ok else "0.0%",
        },
        {
            "metric": "drift_rate",
            "value": f"{(drift_true / ok * 100.0):.1f}%" if ok else "0.0%",
        },
    ]

    for k in ["sound", "questionable", "unsound"]:
        summary_rows.append({"metric": f"moral_status_{k}", "value": status_counter.get(k, 0)})

    write_csv(Path(args.summary_csv), ["metric", "value"], summary_rows)

    by_group = {}
    for r in ok_rows:
        gid = r.get("group_id") or "NO_GROUP"
        by_group.setdefault(gid, []).append(r)

    group_rows = []
    for gid in sorted(by_group.keys()):
        group_items = by_group[gid]
        group_total = len(group_items)
        group_supports = sum(1 for x in group_items if x["audit"].get("supports_atom") is True)
        group_drift = sum(1 for x in group_items if x["audit"].get("drift_detected") is True)
        group_status = Counter(x["audit"].get("moral_status", "unknown") for x in group_items)

        group_rows.append(
            {
                "group_id": gid,
                "rows": group_total,
                "supports_true": group_supports,
                "supports_rate": f"{(group_supports / group_total * 100.0):.1f}%" if group_total else "0.0%",
                "drift_true": group_drift,
                "drift_rate": f"{(group_drift / group_total * 100.0):.1f}%" if group_total else "0.0%",
                "sound": group_status.get("sound", 0),
                "questionable": group_status.get("questionable", 0),
                "unsound": group_status.get("unsound", 0),
            }
        )

    write_csv(
        Path(args.groups_csv),
        [
            "group_id",
            "rows",
            "supports_true",
            "supports_rate",
            "drift_true",
            "drift_rate",
            "sound",
            "questionable",
            "unsound",
        ],
        group_rows,
    )

    top_issues = issues_counter.most_common(10)

    lines = []
    lines.append("============================================================")
    lines.append("REASONING LOOP SUMMARY")
    lines.append("============================================================")
    lines.append("")
    lines.append(f"Total rows: {total}")
    lines.append(f"Audited rows: {ok}")
    if ok:
        lines.append(
            f"Supports atom (true): {supports_true} ({(supports_true / ok * 100.0):.1f}%)"
        )
        lines.append(
            f"Drift detected (true): {drift_true} ({(drift_true / ok * 100.0):.1f}%)"
        )
    else:
        lines.append("Supports atom (true): 0")
        lines.append("Drift detected (true): 0")
    lines.append("")
    lines.append("Moral status counts")
    lines.append("-------------------")
    for k in ["sound", "questionable", "unsound"]:
        lines.append(f"{k}: {status_counter.get(k, 0)}")
    lines.append("")
    lines.append("Top issue tags")
    lines.append("--------------")
    if top_issues:
        for issue, count in top_issues:
            lines.append(f"{issue}: {count}")
    else:
        lines.append("none")
    lines.append("")
    lines.append("Outputs")
    lines.append("-------")
    lines.append(f"Summary CSV: {args.summary_csv}")
    lines.append(f"Group CSV:   {args.groups_csv}")
    lines.append("============================================================")

    write_text(Path(args.summary_txt), "\n".join(lines) + "\n")

    print(f"Loaded {total} audit rows ({ok} valid).")
    print(f"Wrote {args.summary_csv}, {args.groups_csv}, and {args.summary_txt}")


if __name__ == "__main__":
    main()
