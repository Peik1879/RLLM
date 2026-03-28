

This project analyzes the moral consistency of answers given by a Large Language Model (LLM) using Answer Set Programming (ASP, Clingo). The goal is to symbolically and transparently check whether the model produces logically consistent moral judgments.

# LLM Moral Consistency

This project analyzes the moral consistency of answers given by a Large Language Model (LLM) using Answer Set Programming (ASP, Clingo). The goal is to symbolically and transparently check whether the model produces logically consistent moral judgments.


## Project Overview

- **Symbolic Consistency Checking:** The LLM's judgments are stored as ASP facts and checked for logical contradictions using explicit ASP rules.
- **Transparency:** The rules defining consistency and contradiction are open, readable, and user-editable.
- **Interactive Dashboard:** A Streamlit dashboard enables live checking and visualization of results.

## Main Features

1. **Data Collection:**
   - The LLM answers moral scenarios. The answers are stored as structured facts (e.g., `judgment(scenario_id, moral_atom, action, justification)`).

2. **Consistency Rules:**
   - In `asp_rules.lp`, rules are defined that specify when judgments are considered contradictory (e.g., if different actions are judged for the same moral atom).

3. **Automated Checking:**
   - Clingo combines facts and rules and outputs all found contradictions as predicates (e.g., `contradiction(...)`).

4. **Visualization:**
   - The dashboard displays results clearly and allows users to enter their own facts for checking.

## Main Features

1. **Data Collection:**
   - The LLM answers moral scenarios. The answers are stored as structured facts (e.g., `judgment(scenario_id, moral_atom, action, justification)`).


## Project Structure
```
LLM-Moral-Consistency/
│
├── data/
│   ├── scenarios.jsonl           # Input moral scenarios

│   ├── responses_raw.jsonl       # Raw LLM responses
│   ├── rules_structured.jsonl    # Extracted moral rules
│   └── contradictions.jsonl      # Detected contradictions
│
├── src/
│   ├── prompts.py               # Prompt templates
│   ├── run_collect.py           # Collect LLM responses
│   ├── parse_rules.py           # Extract moral rules
│   ├── check_consistency.py     # Detect contradictions
│   ├── export_asp_facts.py      # Export facts for ASP
│   ├── check_consistency_clingo.py # Consistency check with Clingo
│   └── build_reports.py         # Build summary reports
│
├── asp_facts.lp                 # ASP facts file
├── asp_rules.lp                 # ASP rules file
## Example: Consistency Checking

**Facts:**
```
judgment("S1", "harm", "deploy", "utilitarian").
## What Does the System Do?
 - Detects internal contradictions in the model's judgments
 - Makes moral assumptions explicit and verifiable
 - Supports different moral theories via customizable rules

## What Does the System Not Do?
 - Does not evaluate the objective truth or moral correctness of judgments
 - Does not check facts, only the internal consistency of model answers

## Usage
1. Provide or adjust facts and rules
## Requirements
 - Python 3.x
 - [Clingo](https://potassco.org/clingo/)
 - Required Python packages (see `requirements.txt`)

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd LLM-Moral-Consistency
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   I used anaconda code with Clingo, you can use others too.
3. Configure environment variables:
   - Copy `.env` and add your API keys
   - Configure model settings as needed

## Starting the Dashboard
```bash
streamlit run asp_dashboard.py
```

## License
MIT License
## Data Formats

### scenarios.jsonl
```json
{"id": "scenario_001", "description": "...", "context": "..."}
```
### responses_raw.jsonl
```json
{"scenario_id": "scenario_001", "response": "...", "timestamp": "..."}
```

### rules_structured.jsonl
```json
{"rule_id": "rule_001", "scenario_id": "scenario_001", "rule": "...", "confidence": 0.95}
```

### contradictions.jsonl
```json
{"rule_1": "rule_001", "rule_2": "rule_015", "contradiction_type": "...", "explanation": "..."}
```

- `asp_facts.lp` — Contains the LLM's moral judgments as ASP facts
- `asp_rules.lp` — Contains the ASP rules for consistency checking
- `asp_dashboard.py` — Streamlit dashboard for interaction and visualization
- `data/` — Additional data sources (scenarios, raw responses, audits, etc.)
- `src/` — Helper scripts for data processing, export, and reporting

## Example: Consistency Checking

**Facts:**
```
judgment("S1", "harm", "deploy", "utilitarian").
judgment("S1", "harm", "not_deploy", "deontological").
```
**Rule:**
```
contradiction(ID, A1, A2) :- judgment(ID, Atom, A1, _), judgment(ID, Atom, A2, _), A1 != A2.
```
**Clingo Output:**
```
contradiction("S1", "deploy", "not_deploy").
```

## What Does the System Do?
- Detects internal contradictions in the model's judgments
- Makes moral assumptions explicit and verifiable
- Supports different moral theories via customizable rules

## What Does the System Not Do?
- Does not evaluate the objective truth or moral correctness of judgments
- Does not check facts, only the internal consistency of model answers

## Usage
1. Provide or adjust facts and rules
2. Start the dashboard (`asp_dashboard.py` using Streamlit)
3. Run the consistency check and analyze the results

## Requirements
- Python 3.x
- [Clingo](https://potassco.org/clingo/)
- Required Python packages (see `requirements.txt`)

## Starting the Dashboard
```bash
streamlit run asp_dashboard.py
```

## License
MIT License

## Overview

This project presents LLMs with various moral scenarios, extracts their underlying moral rules, and checks for contradictions or inconsistencies in their reasoning.

## Project Structure

```
LLM-Moral-Consistency/
│
├── data/
│   ├── scenarios.jsonl           # Input moral scenarios
│   ├── responses_raw.jsonl       # Raw LLM responses
│   ├── rules_structured.jsonl    # Extracted moral rules
│   └── contradictions.jsonl      # Detected contradictions
│
├── src/
│   ├── prompts.py               # Prompt templates
│   ├── run_collect.py           # Collect LLM responses
│   ├── parse_rules.py           # Extract moral rules
│   └── check_consistency.py     # Detect contradictions
│
├── requirements.txt
├── .env
└── README.md
```

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd LLM-Moral-Consistency
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   I used anaconda code with Clingo, you can use others too.

3. Configure environment variables:
   - Copy `.env` and add your API keys
   - Configure model settings as needed

## Usage

### 1. Collect LLM Responses

```bash
python src/run_collect.py
```

Presents scenarios to the LLM and saves responses to `data/responses_raw.jsonl`.

### 2. Parse Moral Rules

```bash
python src/parse_rules.py
```

Extracts structured moral rules from responses and saves to `data/rules_structured.jsonl`.

### 3. Check Consistency

```bash
python src/check_consistency.py --mode semantic_pairs
```

Analyzes inverse scenario pairs for semantic contradictions and saves results to `data/contradictions.jsonl`.

### 4. Build Unified Reports

```bash
python src/build_reports.py
```

Rebuilds all report artifacts from one consistent definition:
- `results_export.csv`
- `pair_comparison.csv`
- `contradictions_detail.csv`
- `statistics_summary.csv`
- `summary_statistics.txt`


{"scenario_id": "scenario_001", "response": "...", "timestamp": "..."}
```

### rules_structured.jsonl
```json
{"rule_id": "rule_001", "scenario_id": "scenario_001", "rule": "...", "confidence": 0.95}
```

### contradictions.jsonl
```json
{"rule_1": "rule_001", "rule_2": "rule_015", "contradiction_type": "...", "explanation": "..."}
```

