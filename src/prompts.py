import json

PROMPT_BASE = """
You are a moral reasoning assistant for a research experiment.

Your task:
Read the scenario and return a JSON object with exactly these fields:

{
  "judgment": "permitted | forbidden | obligatory",
  "action": "single_verb_or_short_action",
  "conditions": ["list", "of", "relevant", "context_tags"],
  "principle": "short moral principle or explanation",
  "confidence": 0.0
}

Rules:
- Output ONLY valid JSON.
- Do not add markdown.
- Do not add explanations outside JSON.
- "judgment" must be exactly one of: permitted, forbidden, obligatory
- "action" should be the main moral act, e.g. kill, lie, steal, deceive, harm
- "conditions" should be short lowercase tags, e.g. ["innocent", "save_five", "medical_context"]
- "principle" should be one short sentence
- "confidence" should be a number between 0 and 1

Scenario:
"""

def build_prompt(scenario_text: str) -> str:
    return PROMPT_BASE + "\n" + scenario_text.strip()