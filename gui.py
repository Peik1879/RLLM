import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import os
from clingo_runner import run_clingo
from parser import parse_clingo_output

FACTS_FILE = "facts.lp"
RULES_FILE = "rules.lp"

EXAMPLE_FACTS = """judgment(1, lying, allow, protect_life).
judgment(1, lying, forbid, truth).
"""

EXAMPLE_RULES = """contradiction(S, A) :-
    judgment(S, A, allow, _),
    judgment(S, A, forbid, _).
"""

class ConsistencyCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Symbolic Consistency Checker for Moral Judgments")
        self.create_widgets()
        self.load_files()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Facts editor
        ttk.Label(left_frame, text="facts.lp").pack(anchor=tk.W)
        self.facts_text = ScrolledText(left_frame, width=40, height=20)
        self.facts_text.pack(fill=tk.BOTH, expand=True)

        # Rules editor
        ttk.Label(right_frame, text="rules.lp").pack(anchor=tk.W)
        self.rules_text = ScrolledText(right_frame, width=40, height=20)
        self.rules_text.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Check Consistency", command=self.check_consistency).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Load Example", command=self.load_example).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)

        # Output area
        output_frame = ttk.LabelFrame(self.root, text="Contradictions", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.output_tree = ttk.Treeview(output_frame, columns=("Scenario", "Action", "Status"), show="headings")
        self.output_tree.heading("Scenario", text="Scenario")
        self.output_tree.heading("Action", text="Action")
        self.output_tree.heading("Status", text="Status")
        self.output_tree.pack(fill=tk.BOTH, expand=True)


        # Explanations output as scrollable list
        expl_frame = ttk.LabelFrame(self.root, text="Erklärungen", padding="5")
        expl_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,5))
        self.explanation_tree = ttk.Treeview(expl_frame, columns=("Scenario", "Action", "Type"), show="headings", height=8)
        self.explanation_tree.heading("Scenario", text="Szenario")
        self.explanation_tree.heading("Action", text="Aktion")
        self.explanation_tree.heading("Type", text="Typ")
        self.explanation_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        expl_scroll = ttk.Scrollbar(expl_frame, orient="vertical", command=self.explanation_tree.yview)
        self.explanation_tree.configure(yscrollcommand=expl_scroll.set)
        expl_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Moralische Sieger Statistik
        self.stats_label = ttk.Label(output_frame, text="", foreground="darkgreen", anchor="w", justify="left")
        self.stats_label.pack(fill=tk.BOTH, expand=True, pady=(0,0))

    def load_files(self):
        if os.path.exists(FACTS_FILE):
            with open(FACTS_FILE, "r", encoding="utf-8") as f:
                self.facts_text.delete("1.0", tk.END)
                self.facts_text.insert(tk.END, f.read())
        if os.path.exists(RULES_FILE):
            with open(RULES_FILE, "r", encoding="utf-8") as f:
                self.rules_text.delete("1.0", tk.END)
                self.rules_text.insert(tk.END, f.read())

    def save_files(self):
        with open(FACTS_FILE, "w", encoding="utf-8") as f:
            f.write(self.facts_text.get("1.0", tk.END).strip() + "\n")
        with open(RULES_FILE, "w", encoding="utf-8") as f:
            f.write(self.rules_text.get("1.0", tk.END).strip() + "\n")

    def check_consistency(self):
        self.save_files()
        try:
            output = run_clingo(FACTS_FILE, RULES_FILE)
            result = parse_clingo_output(output)
            contradictions = result.get("contradictions", [])
            explanations = result.get("explanations", [])
            # Statistik berechnen
            stats_text = self.calculate_priority_stats()
            self.display_results(contradictions, explanations, stats_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check consistency:\n{e}")

    def display_results(self, contradictions, explanations, stats_text):
        for row in self.output_tree.get_children():
            self.output_tree.delete(row)
        if not contradictions:
            self.output_tree.insert("", tk.END, values=("-", "-", "No contradictions"))
        else:
            for c in contradictions:
                self.output_tree.insert("", tk.END, values=(c["scenario"], c["action"], c["status"]))
        # Show explanations

        # Show explanations in scrollable list
        for row in self.explanation_tree.get_children():
            self.explanation_tree.delete(row)
        if explanations:
            for e in explanations:
                self.explanation_tree.insert("", tk.END, values=(e['scenario'], e['action'], e['type']))

        # Show stats
        self.stats_label.config(text=stats_text)

    def calculate_priority_stats(self):
        from collections import defaultdict
        import re
        priorities = {}
        try:
            with open(FACTS_FILE, encoding="utf-8") as f:
                for line in f:
                    m = re.match(r"priority\(([^,]+),\s*(\d+)\)", line)
                    if m:
                        priorities[m.group(1)] = int(m.group(2))
        except Exception:
            return ""
        judgments = []
        try:
            with open(FACTS_FILE, encoding="utf-8") as f:
                for line in f:
                    m = re.match(r"judgment\((\d+),\s*([^,]+),\s*([^,]+),\s*([^\)]+)\)", line)
                    if m:
                        judgments.append({
                            "scenario": m.group(1),
                            "action": m.group(2),
                            "value": m.group(3),
                            "context": m.group(4)
                        })
        except Exception:
            return ""
        win_stats = defaultdict(int)
        resolved_by_priority = 0
        total_conflicts = 0
        for j in judgments:
            if j["value"] == "allow":
                for k in judgments:
                    if (
                        k["scenario"] == j["scenario"] and
                        k["action"] == j["action"] and
                        k["value"] == "forbid"
                    ):
                        total_conflicts += 1
                        p_allow = priorities.get(j["context"], 0)
                        p_forbid = priorities.get(k["context"], 0)
                        if p_allow > p_forbid:
                            win_stats[j["context"]] += 1
                            resolved_by_priority += 1
                        elif p_forbid > p_allow:
                            win_stats[k["context"]] += 1
                            resolved_by_priority += 1
        if total_conflicts == 0:
            return ""
        stats = f"--- Statistik: Konfliktauflösung durch Prioritäten ---\n"
        stats += f"Gesamtzahl Konflikte: {total_conflicts}\n"
        stats += f"Davon durch Prioritäten aufgelöst: {resolved_by_priority}\n"
        stats += "\nKontext              | Konflikte entschieden\n"
        stats += "------------------------------\n"
        for ctx, count in sorted(win_stats.items(), key=lambda x: -x[1]):
            stats += f"{ctx:20} | {count}\n"
        return stats

    def load_example(self):
        self.facts_text.delete("1.0", tk.END)
        self.facts_text.insert(tk.END, EXAMPLE_FACTS)
        self.rules_text.delete("1.0", tk.END)
        self.rules_text.insert(tk.END, EXAMPLE_RULES)

    def reset(self):
        self.facts_text.delete("1.0", tk.END)
        self.rules_text.delete("1.0", tk.END)
        self.output_tree.delete(*self.output_tree.get_children())

if __name__ == "__main__":
    root = tk.Tk()
    app = ConsistencyCheckerGUI(root)
    root.mainloop()
