import argparse
import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


def read_results_csv(path: Path):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def read_pair_csv(path: Path):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def plot_judgment_distribution(results_rows, out_path: Path):
    judgments = [r["judgment"].strip().lower() for r in results_rows]
    counts = Counter(judgments)

    labels = sorted(counts.keys())
    values = [counts[l] for l in labels]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values)
    plt.title("Judgment Distribution")
    plt.xlabel("Judgment")
    plt.ylabel("Count")
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.05, str(value), ha="center")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_category_distribution(results_rows, out_path: Path):
    categories = [r["category"].strip().lower() for r in results_rows]
    counts = Counter(categories)

    labels = sorted(counts.keys())
    values = [counts[l] for l in labels]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(labels, values)
    plt.title("Category Distribution")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=25, ha="right")
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.05, str(value), ha="center")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_confidence_analysis(results_rows, out_path: Path):
    confidences = [float(r["confidence"]) for r in results_rows]

    avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
    min_conf = min(confidences) if confidences else 0.0
    max_conf = max(confidences) if confidences else 0.0

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    axes[0].hist(confidences, bins=8)
    axes[0].set_title("Confidence Histogram")
    axes[0].set_xlabel("Confidence")
    axes[0].set_ylabel("Frequency")

    metric_labels = ["Min", "Average", "Max"]
    metric_values = [min_conf, avg_conf, max_conf]
    bars = axes[1].bar(metric_labels, metric_values)
    axes[1].set_ylim(0, 1.05)
    axes[1].set_title("Confidence Summary")
    for bar, value in zip(bars, metric_values):
        axes[1].text(bar.get_x() + bar.get_width() / 2, value + 0.02, f"{value:.3f}", ha="center")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_contradictions_summary(pair_rows, out_path: Path):
    total_pairs = len(pair_rows)
    consistent = sum(1 for r in pair_rows if r["consistent"].strip().lower() == "yes")
    contradictions = total_pairs - consistent

    labels = ["Semantically Contradictory", "Consistent"]
    values = [contradictions, consistent]

    plt.figure(figsize=(7, 5))
    wedges, texts, autotexts = plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title(f"Contradictions Summary ({contradictions}/{total_pairs} contradictory)")
    for t in autotexts:
        t.set_color("white")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", default="results_export.csv")
    parser.add_argument("--pairs", default="pair_comparison.csv")
    parser.add_argument("--out-dir", default=".")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results_rows = read_results_csv(Path(args.results))
    pair_rows = read_pair_csv(Path(args.pairs))

    plot_judgment_distribution(results_rows, out_dir / "judgment_distribution.png")
    plot_confidence_analysis(results_rows, out_dir / "confidence_analysis.png")
    plot_category_distribution(results_rows, out_dir / "category_distribution.png")
    plot_contradictions_summary(pair_rows, out_dir / "contradictions_summary.png")

    print(f"Generated plots in {out_dir}")


if __name__ == "__main__":
    main()
