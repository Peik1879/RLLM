import subprocess

def run_clingo(facts_path, rules_path):
    cmd = ["clingo", facts_path, rules_path, "--outf=2"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
