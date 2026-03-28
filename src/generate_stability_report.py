#!/usr/bin/env python3
"""Generate a beautiful HTML report of stability analysis."""

import json
from pathlib import Path


def main():
    data = [
        json.loads(line)
        for line in Path("data/group_audit.jsonl").read_text().split("\n")
        if line.strip()
    ]

    def sort_key(r):
        a = r.get("audit", {})
        n_pairs = len(a.get("contradiction_pairs", []))
        severity_rank = {"low": 0, "medium": 1, "high": 2}
        sev = severity_rank.get(a.get("severity", "high"), 2)
        return (n_pairs, sev)

    sorted_data = sorted(data, key=sort_key)

    html_rows = ""
    for idx, r in enumerate(sorted_data, 1):
        gid = r["group_id"]
        cat = r["category"].replace("_", " ").title()
        a = r.get("audit", {})

        pairs = a.get("contradiction_pairs", [])
        n_pairs = len(pairs)
        severity = a.get("severity", "?").upper()

        # Score
        if n_pairs == 1:
            score_class = "high-stable"
            score_text = f"{n_pairs} Widerspruch"
        elif n_pairs == 2:
            score_class = "medium-stable"
            score_text = f"{n_pairs} Widersprüche"
        else:
            score_class = "low-stable"
            score_text = f"{n_pairs} Widersprüche"

        # Pairs
        pairs_html = ""
        for pair in pairs:
            pairs_html += f"<strong>{pair[0]}</strong> ↔ <strong>{pair[1]}</strong><br>"

        # Severity
        if severity == "HIGH":
            severity_color = "#e74c3c"
            severity_label = "⚠️ HOCH"
        elif severity == "MEDIUM":
            severity_color = "#f39c12"
            severity_label = "⚡ MITTEL"
        else:
            severity_color = "#27ae60"
            severity_label = "✓ GERING"

        html_rows += f"""
            <tr>
                <td class="rank">#{idx}</td>
                <td class="group-id">{gid}<br><span style="font-size: 12px; color: #999; font-weight: normal;">{cat}</span></td>
                <td><div class="stability-bar {score_class}">{score_text}</div></td>
                <td class="contradiction-list">{pairs_html}</td>
                <td style="color: {severity_color}; font-weight: 600;">{severity_label}</td>
            </tr>
"""

    html_template = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moralische Stabilitätsanalyse</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f7fa;
            color: #1a1a1a;
        }}
        h1 {{ 
            text-align: center;
            color: #0066cc;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }}
        .summary-box {{
            background: white;
            border-left: 4px solid #0066cc;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-box h3 {{
            margin-top: 0;
            color: #0066cc;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 40px;
        }}
        th {{
            background: #0066cc;
            color: white;
            padding: 16px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #003d99;
        }}
        td {{
            padding: 14px 16px;
            border-bottom: 1px solid #e0e0e0;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        tr:hover {{
            background: #f9f9f9;
        }}
        .rank {{
            font-weight: 600;
            font-size: 16px;
            width: 40px;
        }}
        .stable {{ color: #27ae60; font-weight: 600; }}
        .unstable {{ color: #e74c3c; font-weight: 600; }}
        .medium {{ color: #f39c12; font-weight: 600; }}
        .group-id {{
            font-weight: 600;
            color: #0066cc;
        }}
        .stability-bar {{
            display: inline-flex;
            height: 24px;
            border-radius: 3px;
            color: white;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 600;
            min-width: 60px;
        }}
        .high-stable {{ background: #27ae60; }}
        .medium-stable {{ background: #f39c12; }}
        .low-stable {{ background: #e74c3c; }}
        .contradiction-list {{
            font-size: 13px;
            color: #666;
            line-height: 1.4;
        }}
        .contradiction-list strong {{
            color: #0066cc;
        }}
        .legend {{
            background: white;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .legend h3 {{
            margin-top: 0;
            color: #0066cc;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 30px;
            margin-bottom: 10px;
        }}
        .legend-box {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 3px;
            margin-right: 8px;
            vertical-align: middle;
        }}
        footer {{
            text-align: center;
            color: #999;
            margin-top: 50px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <h1>🧠 Moralische Stabilitätsanalyse</h1>
    <p class="subtitle">Wie stabil sind LLM-Urteile unter verschiedenen ethischen Rahmungen?</p>
    
    <div class="legend">
        <h3>Was bedeutet die Stabilität?</h3>
        <div class="legend-item">
            <span class="legend-box" style="background: #27ae60;"></span>
            <strong>Stabil (1 Widerspruch)</strong> — Fast alle Rahmungen führen zu demselben Urteil
        </div>
        <div class="legend-item">
            <span class="legend-box" style="background: #f39c12;"></span>
            <strong>Mittel (2 Widersprüche)</strong> — Mehrere Framework-Paare widersprechen sich
        </div>
        <div class="legend-item">
            <span class="legend-box" style="background: #e74c3c;"></span>
            <strong>Instabil (3+ Widersprüche)</strong> — Viele gegensätzliche Urteile, sehr framingabhängig
        </div>
    </div>
    
    <div class="summary-box">
        <h3>📊 Überblick</h3>
        <p><strong>Untersuchte Szenen:</strong> 10 Themenbereiche × 5 ethische Rahmungen = 50 Szenarien</p>
        <p><strong>Stabilitätsergebnis:</strong></p>
        <ul>
            <li><span class="stable">✓ 1 Gruppe stabiler</span> (G07 — Flüchtlingspolitik)</li>
            <li><span class="medium">⚡ 8 Gruppen mittelmäßig instabil</span> (2 Widerspruchspaare)</li>
            <li><span class="unstable">⚠️ 1 Gruppe hochinstabil</span> (G01 — Autonome Waffen, 3 Widersprüche)</li>
        </ul>
        <p><strong>Kernbefund:</strong> <strong>Keine Stabilitäts-Position</strong> — Ein KI-Modell hat zu keiner einzigen ethischen Frage eine geschlossene, rahmenunabhängige moralische Position.</p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Rang</th>
                <th>Thema</th>
                <th>Stabilitäts-Score</th>
                <th>Widersprechende Framework-Paare</th>
                <th>Schwere</th>
            </tr>
        </thead>
        <tbody>
{html_rows}
        </tbody>
    </table>

    <div class="summary-box">
        <h3>🔍 Muster in den Daten</h3>
        <p><strong>Am häufigsten widersprechen sich Diese Framework-Paare:</strong></p>
        <ul>
            <li><strong>Utilitarismus ↔ Deontologie</strong> — 9/10 Gruppen im Konflikt<br>
                <span style="font-size: 13px; color: #666;">„Größtes Glück" vs. „moralische Pflicht" — KI kann sich nicht einigen</span></li>
            <li><strong>Emotional ↔ Statistisch</strong> — 9/10 Gruppen im Konflikt<br>
                <span style="font-size: 13px; color: #666;">„Bauchgefühl" vs. „objektive Daten" — KI sagt unterschiedliches</span></li>
            <li><strong>Utilitarian ↔ Authority</strong> — 1/10 Gruppen im Konflikt (G08: Todesstrafe)<br>
                <span style="font-size: 13px; color: #666;">Seltener in Konflikt, meist eher komplementär</span></li>
        </ul>
        <p><strong>Ausreißer:</strong> G07 (Flüchtlingspolitik) zeigt weniger Widersprüche — warum? Vermutung: Dieses Thema hat konsistenteren intuitiven Konsens über Frameworks hinweg, oder die generierte Atome waren zufällig ähnlicher.</p>
    </div>

    <footer>
        Generated automatically from group_audit.jsonl | Auditor: qwen2.5:7b | Date: 2026-03-13
    </footer>
</body>
</html>
"""

    Path("stability_analysis.html").write_text(html_template, encoding="utf-8")
    print("✅ stability_analysis.html erstellt")
    print("📂 Dateipfad: stability_analysis.html")


if __name__ == "__main__":
    main()
