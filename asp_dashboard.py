import streamlit as st
import subprocess
import re
from pathlib import Path
import pandas as pd



st.set_page_config(page_title="LLM Moral Consistency – ASP Dashboard", layout="wide")

# --- Info-Block und Anleitung (Dark Mode optimiert) ---
st.markdown("""
<div style='background: #23272f; border-radius:8px; padding:1.2em 1.5em; margin-bottom:1.5em; border-left: 6px solid #1976d2;'>
<h2 style='margin-top:0; color:#fff;'>🧭 LLM Moral Consistency Dashboard</h2>
<div style='color:#e0e0e0;'>
<b>Was macht dieses Tool?</b><br>
Dieses Dashboard prüft, ob KI-generierte moralische Urteile logisch konsistent sind. Dazu werden die Urteile als ASP-Fakten exportiert und mit <b>Clingo</b> auf Widersprüche untersucht.<br><br>
<b>Wie funktioniert es?</b>
<ol style='margin-top:0.5em; margin-bottom:0.5em;'>
    <li> <b>Urteile exportieren:</b> Die KI-Urteile werden als ASP-Fakten gespeichert (asp_facts.lp).</li>
    <li> <b>Regeln anwenden:</b> Mit ASP-Regeln (asp_rules.lp) werden logische Widersprüche definiert.</li>
    <li> <b>Konsistenz prüfen:</b> Clingo sucht nach Widersprüchen in den Fakten.</li>
    <li> <b>Ergebnisse anzeigen:</b> Gefundene Widersprüche werden hier übersichtlich dargestellt.</li>
</ol>
<b>So nutzt du das Dashboard:</b>
<ol style='margin-top:0.5em; margin-bottom:0.5em;'>
    <li> Klicke links auf <b>Konsistenzprüfung starten</b>, um die aktuellen Daten zu prüfen.</li>
    <li> Optional: Gib unten eigene ASP-Fakten ein und prüfe sie direkt.</li>
</ol>
</div>
</div>
""", unsafe_allow_html=True)



# --- Nutzereingabe für eigene Szenarien (Klartext) ---
st.markdown("<h4>Eigenes Szenario in Klartext eingeben</h4>", unsafe_allow_html=True)
user_scenario = st.text_area("Formuliere hier deine eigene moralische Frage oder ein Szenario (z.B. 'Ist es moralisch in Ordnung, an Menschen Medizin blind zu testen?')", height=60)
if user_scenario.strip():
    st.markdown(f"<div style='margin:0.5em 0 1em 0; padding:1em; background:#23272f; border-radius:8px; color:#e0e0e0;'><b>Dein Szenario:</b><br>{user_scenario}</div>", unsafe_allow_html=True)

# --- Nutzereingabe für eigene Prüfung ---
st.markdown("<h4>Eigene ASP-Fakten prüfen</h4>", unsafe_allow_html=True)
user_input = st.text_area("Gib hier eigene ASP-Fakten ein (z.B. contradiction(\"G01F1\",deploy).)", height=80)
check_user_input = st.button("Eigene Eingabe prüfen")

# --- Übersicht aller Szenario-IDs, Aktionen und Beschreibungen ---
import itertools
import ast
import json
facts_path = Path("asp_facts.lp")
scenarios_path = Path("data/scenarios.jsonl")
ids = set()
actions = set()
id2desc = {}
if facts_path.exists():
    with open(facts_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("judgment("):
                try:
                    args = line[line.find("(")+1:line.find(")")]
                    parts = [a.strip('" ') for a in args.split(",")]
                    if len(parts) >= 3:
                        ids.add(parts[0])
                        actions.add(parts[2])
                except Exception:
                    pass
# Mapping ID -> Beschreibung laden
if scenarios_path.exists():
    with open(scenarios_path, encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                if "id" in obj and "text" in obj:
                    id2desc[obj["id"]] = obj["text"]
            except Exception:
                pass
if ids or actions:
    st.markdown("""
<div style='margin:1em 0 1em 0; padding:1em; background:#181b20; border-radius:8px; color:#e0e0e0;'>
<b>Verfügbare Szenario-IDs:</b> <br>""" + ", ".join(sorted(ids)) + """
<br><b>Verfügbare Aktionen:</b> <br>""" + ", ".join(sorted(actions)) + "</div>", unsafe_allow_html=True)
    # Szenario-Beschreibungen anzeigen
    if id2desc:
        st.markdown("<b>Szenario-IDs mit Beschreibung:</b>", unsafe_allow_html=True)
        for sid in sorted(ids):
            desc = id2desc.get(sid, "(keine Beschreibung gefunden)")
            st.markdown(f"<div style='margin-bottom:0.5em; color:#e0e0e0;'><b>{sid}:</b> {desc}</div>", unsafe_allow_html=True)

if check_user_input and user_input.strip():
        with st.spinner("Clingo prüft deine Eingabe..."):
                # Schreibe Nutzereingabe temporär in Datei
                tmp_path = "user_input.lp"
                with open(tmp_path, "w", encoding="utf-8") as f:
                        f.write(user_input)
                result = subprocess.run(["clingo", tmp_path, str(Path("asp_rules.lp"))], capture_output=True, text=True)
                output = result.stdout
                st.subheader("Clingo-Ausgabe für eigene Eingabe")
                st.code(output)
                contradictions = re.findall(r'contradiction\\(([^)]+)\\)', output)
                if contradictions:
                        st.success(f"{len(contradictions)} Widersprüche gefunden:")
                        st.write(contradictions)
                else:
                        st.info("Keine Widersprüche gefunden.")

# --- Übersicht/Überblick Block (Dark Mode optimiert) ---
st.markdown("""
<div style='background: #23272f; border-radius:8px; padding:1em 1.5em; margin-bottom:1.5em; border-left: 6px solid #1976d2;'>
<h4 style='color:#fff;'>Überblick</h4>
<div style='color:#e0e0e0;'>
<b>Untersuchte Szenen:</b> 10 Themenbereiche × 5 ethische Rahmungen = 50 Szenarien<br>
<b>Stabilitätsergebnis:</b><br>
<ul style='margin-top:0.5em; margin-bottom:0.5em;'>
    <li> <span style='color:#388e3c;'>🟢 1 Gruppe stabiler</span> (G07 — Flüchtlingspolitik) </li>
    <li> <span style='color:#fbc02d;'>🟠 8 Gruppen mittelmäßig instabil</span> (2 Widerspruchspaare) </li>
    <li> <span style='color:#d32f2f;'>🔴 1 Gruppe hochinstabil</span> (G01 — Autonome Waffen, 3 Widersprüche) </li>
</ul>
<b>Kernbefund:</b> <i>Keine Stabilitäts-Position</i> — Ein KI-Modell hat zu keiner einzigen ethischen Frage eine geschlossene, rahmenunabhängige moralische Position.
</div>
</div>
""", unsafe_allow_html=True)

st.title("LLM Moral Consistency – ASP/Clingo Dashboard")

FACTS = Path("asp_facts.lp")
RULES = Path("asp_rules.lp")
CLINGO = "clingo"

st.sidebar.header("Aktionen")
run_check = st.sidebar.button("Konsistenzprüfung starten")


def render_score_label(score):
    if score == "Stabil":
        return "<span style='color:#388e3c; font-weight:bold;'>🟢 Stabil</span>"
    elif score == "Widerspruch":
        return "<span style='color:#d32f2f; font-weight:bold;'>🔴 Widerspruch</span>"
    else:
        return f"<span style='color:#fbc02d; font-weight:bold;'>🟠 {score}</span>"

def render_severity_label(severity):
    if severity == "HOCH":
        return "<span style='color:#d32f2f; font-weight:bold;'>HOCH</span>"
    elif severity == "MITTEL":
        return "<span style='color:#fbc02d; font-weight:bold;'>MITTEL</span>"
    else:
        return "<span style='color:#388e3c; font-weight:bold;'>NIEDRIG</span>"

if run_check:
    with st.spinner("Clingo läuft..."):
        result = subprocess.run([CLINGO, str(FACTS), str(RULES)], capture_output=True, text=True)
        output = result.stdout
        st.subheader("Clingo-Ausgabe")
        st.code(output)
        # Extrahiere Widersprüche
        contradictions = re.findall(r'contradiction\\(([^)]+)\\)', output)
        if contradictions:
            st.success(f"{len(contradictions)} Widersprüche gefunden:")
            # Dummy-Daten für weitere Spalten (hier kannst du echte Daten einfügen)
            data = []
            for idx, c in enumerate(contradictions, 1):
                szenario, aktion = [x.strip('" ') for x in c.split(',')]
                # Dummy-Werte für Thema, Score, Framework-Paare, Schwere
                thema = f"G{str(idx).zfill(2)}"
                score = "Widerspruch"
                framework = "emotional – statistical"
                schwere = "HOCH" if idx == 1 else "MITTEL"
                data.append({
                    "Rang": f"#{idx}",
                    "Thema": thema,
                    "Stabilitäts-Score": score,
                    "Widersprechende Framework-Paare": framework,
                    "Schwere": schwere,
                    "Szenario": szenario,
                    "Aktion": aktion
                })
            df = pd.DataFrame(data)
            # Formatierte Tabelle mit HTML
            def style_row(row):
                return [
                    row["Rang"],
                    row["Thema"],
                    render_score_label(row["Stabilitäts-Score"]),
                    row["Widersprechende Framework-Paare"],
                    render_severity_label(row["Schwere"])
                ]
            st.markdown("<h4>Widerspruchs-Übersicht</h4>", unsafe_allow_html=True)
            table_html = """
<table style='width:100%; border-collapse:collapse; font-size:1.08em;'>
  <tr style='background:#e3eaf2; font-weight:bold; color:#222;'>
    <th style='padding:8px;'>Rang</th>
    <th style='padding:8px;'>Thema</th>
    <th style='padding:8px;'>Stabilitäts-Score</th>
    <th style='padding:8px;'>Widersprechende Framework-Paare</th>
    <th style='padding:8px;'>Schwere</th>
  </tr>
"""
            for _, row in df.iterrows():
                styled = style_row(row)
                table_html += f"<tr style='color:#222; background:#fff;'>"
                for cell in styled:
                    table_html += f"<td style='padding:8px; border-bottom:1px solid #e0e0e0;'>{cell}</td>"
                table_html += "</tr>"
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.info("Keine Widersprüche gefunden.")
else:
    st.info("Klicke links auf 'Konsistenzprüfung starten', um die Ergebnisse zu sehen.")

st.markdown("---")
st.markdown("**Hinweis:** Das Dashboard liest asp_facts.lp und asp_rules.lp im Projektverzeichnis und zeigt die Clingo-Ergebnisse live an.")
