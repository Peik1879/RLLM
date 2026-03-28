import json

def parse_clingo_output(clingo_json):
    data = json.loads(clingo_json)
    contradictions = []
    explanations = []
    for answer in data.get("Call", [])[0].get("Witnesses", []):
        for atom in answer.get("Value", []):
            if atom.startswith("contradiction("):
                inner = atom[len("contradiction("):-1]
                scenario, action = [x.strip() for x in inner.split(",")]
                contradictions.append({
                    "scenario": scenario,
                    "action": action,
                    "status": "CONTRADICTION"
                })
            elif atom.startswith("explain("):
                inner = atom[len("explain("):-1]
                parts = [x.strip() for x in inner.split(",")]
                if len(parts) == 3:
                    explanations.append({
                        "scenario": parts[0],
                        "action": parts[1],
                        "type": parts[2]
                    })
    return {"contradictions": contradictions, "explanations": explanations}
