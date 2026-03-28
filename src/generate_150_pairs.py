import json
from pathlib import Path


def build_themes():
    return [
        {
            "category": "autonomous_weapons",
            "action": "deploy an autonomous weapon system",
            "benefits": [
                "prevent a larger attack",
                "stop a coordinated strike",
                "protect allied civilians",
                "disable a hostile launch site",
                "prevent mass casualties",
                "intercept armed vehicles",
                "protect a humanitarian corridor",
                "prevent escalation at the border",
                "stop repeated drone attacks",
                "protect a crowded evacuation route",
            ],
            "costs": [
                "nearby civilians may be harmed",
                "the target identification is imperfect",
                "non-combatants could be misclassified",
                "there is limited human oversight",
                "collateral damage is possible",
                "accountability for mistakes is unclear",
                "the system may fail in edge cases",
                "the data used for targeting may be biased",
                "civilian infrastructure may be hit",
                "operators may react too late to abort",
            ],
        },
        {
            "category": "surveillance",
            "action": "introduce total digital surveillance",
            "benefits": [
                "prevent terrorism",
                "disrupt organized crime",
                "identify violent plots early",
                "improve emergency response",
                "track coordinated cyberattacks",
                "reduce large-scale fraud",
                "protect critical infrastructure",
                "detect extremist networks",
                "find missing persons faster",
                "improve public safety metrics",
            ],
            "costs": [
                "civil liberties are severely reduced",
                "privacy rights are undermined",
                "citizens are constantly monitored",
                "dissent may be chilled",
                "abuse by authorities is possible",
                "data breaches could expose everyone",
                "minorities may be disproportionately targeted",
                "oversight is difficult to enforce",
                "trust in institutions may decline",
                "private life becomes non-existent",
            ],
        },
        {
            "category": "medical_triage",
            "action": "prioritize one patient over another in triage",
            "benefits": [
                "maximize lives saved",
                "improve survival odds overall",
                "preserve scarce ICU capacity",
                "stabilize the emergency ward",
                "treat the most salvageable cases first",
                "avoid system collapse",
                "reduce preventable deaths",
                "focus on highest expected benefit",
                "allocate ventilators efficiently",
                "save more critical patients",
            ],
            "costs": [
                "one patient with lower odds is deprioritized",
                "some families perceive unfairness",
                "the decision can feel discriminatory",
                "individual dignity may feel compromised",
                "late arrivals may lose access",
                "moral distress for clinicians increases",
                "public trust may be harmed",
                "errors in prognosis can occur",
                "people with disabilities may be disadvantaged",
                "appeals cannot be handled in time",
            ],
        },
        {
            "category": "whistleblowing",
            "action": "leak internal documents to expose wrongdoing",
            "benefits": [
                "reveal systemic corruption",
                "prevent ongoing harm",
                "protect affected communities",
                "force institutional accountability",
                "stop illegal practices",
                "inform the public",
                "enable legal intervention",
                "prevent financial exploitation",
                "protect vulnerable workers",
                "expose safety violations",
            ],
            "costs": [
                "classified information may be exposed",
                "national security claims may be affected",
                "individual privacy may be violated",
                "trust inside institutions may erode",
                "sources may face retaliation",
                "documents may be misinterpreted",
                "ongoing investigations may be disrupted",
                "legal obligations may be broken",
                "innocent employees may be implicated",
                "diplomatic relations may be strained",
            ],
        },
        {
            "category": "environmental_policy",
            "action": "ban high-emission industries immediately",
            "benefits": [
                "cut emissions quickly",
                "reduce climate risk",
                "improve air quality",
                "protect future generations",
                "lower health burdens",
                "prevent ecosystem collapse",
                "align with scientific targets",
                "reduce disaster exposure",
                "accelerate green transition",
                "signal strong climate leadership",
            ],
            "costs": [
                "many jobs are lost in the short term",
                "regional economies may contract",
                "energy prices may rise",
                "small suppliers may fail",
                "workers may face sudden displacement",
                "household costs may increase",
                "public backlash may intensify",
                "implementation capacity is limited",
                "illegal markets may emerge",
                "social inequality may worsen initially",
            ],
        },
        {
            "category": "data_privacy",
            "action": "share anonymized health data for AI research",
            "benefits": [
                "speed up medical discoveries",
                "improve rare disease detection",
                "develop better diagnostics",
                "optimize treatment plans",
                "reduce hospital errors",
                "improve outbreak prediction",
                "support public health planning",
                "improve personalized medicine",
                "reduce long-term care costs",
                "accelerate drug development",
            ],
            "costs": [
                "re-identification remains possible",
                "consent may be incomplete",
                "patients may lose control over data",
                "commercial misuse may occur",
                "security breaches are possible",
                "bias in datasets may harm minorities",
                "data governance is uneven",
                "trust in hospitals may decline",
                "cross-border transfer risks increase",
                "oversight mechanisms may lag",
            ],
        },
        {
            "category": "refugee_policy",
            "action": "open emergency borders to refugees",
            "benefits": [
                "save lives immediately",
                "prevent humanitarian catastrophe",
                "protect children in danger",
                "uphold asylum obligations",
                "reduce deaths at sea",
                "stabilize regional camps",
                "support human rights commitments",
                "prevent family separation",
                "reduce exploitation by traffickers",
                "enable urgent medical support",
            ],
            "costs": [
                "local services become strained",
                "housing shortages may worsen",
                "integration systems may be overloaded",
                "political tensions may increase",
                "screening capacity may be insufficient",
                "municipal budgets may be stretched",
                "social cohesion may be challenged",
                "processing delays may increase",
                "employment competition may intensify",
                "public consent may weaken",
            ],
        },
        {
            "category": "judicial_punishment",
            "action": "impose predictive detention on high-risk suspects",
            "benefits": [
                "prevent violent offenses",
                "reduce repeat harm",
                "protect potential victims",
                "lower homicide risk",
                "stabilize high-risk areas",
                "prevent gang retaliation",
                "interrupt escalating threats",
                "reduce emergency policing pressure",
                "protect witnesses",
                "lower serious crime rates",
            ],
            "costs": [
                "people are detained before conviction",
                "false positives can violate rights",
                "algorithmic bias may influence decisions",
                "due process protections may weaken",
                "public trust in justice may decline",
                "detention may be applied unevenly",
                "legal safeguards may be bypassed",
                "innocent people may be harmed",
                "oversight may be inadequate",
                "civil liberties may erode",
            ],
        },
        {
            "category": "resource_allocation",
            "action": "prioritize scarce resources to younger patients",
            "benefits": [
                "maximize expected life-years",
                "improve long-term social outcomes",
                "increase total years saved",
                "support dependents over a longer horizon",
                "improve aggregate survival benefit",
                "optimize long-term utility",
                "protect future workforce capacity",
                "increase recovery-adjusted outcomes",
                "reduce long-term mortality burden",
                "stabilize population-level prognosis",
            ],
            "costs": [
                "older patients are deprioritized",
                "age discrimination concerns arise",
                "equal dignity is questioned",
                "families may perceive injustice",
                "public trust may be reduced",
                "edge cases become contentious",
                "ethical legitimacy may be challenged",
                "non-age factors may be ignored",
                "bias in life-expectancy estimates may exist",
                "social conflict may increase",
            ],
        },
        {
            "category": "misinformation",
            "action": "remove harmful misinformation from public platforms",
            "benefits": [
                "reduce violence incitement",
                "protect election integrity",
                "prevent medical harm",
                "limit panic during crises",
                "reduce hate-driven mobilization",
                "protect vulnerable communities",
                "improve public information quality",
                "reduce coordinated deception",
                "prevent fraud campaigns",
                "protect emergency response efforts",
            ],
            "costs": [
                "free speech concerns increase",
                "moderation errors may silence legitimate speech",
                "platform power grows further",
                "political neutrality may be questioned",
                "appeals can be slow",
                "journalistic content may be flagged",
                "trust in moderation may decline",
                "state pressure on platforms may rise",
                "rules may be applied inconsistently",
                "public debate may narrow",
            ],
        },
        {
            "category": "bioethics",
            "action": "allow human gene editing to prevent severe disease",
            "benefits": [
                "prevent inherited suffering",
                "reduce lifelong disability",
                "lower rare disease burden",
                "improve quality of life",
                "reduce long-term treatment needs",
                "expand therapeutic options",
                "prevent early mortality",
                "enable healthier childhoods",
                "support families with high genetic risk",
                "accelerate curative medicine",
            ],
            "costs": [
                "long-term side effects are uncertain",
                "ethical boundaries may be crossed",
                "access may be unequal",
                "non-therapeutic enhancement may follow",
                "intergenerational effects are unknown",
                "consent for future children is impossible",
                "regulatory oversight may lag",
                "social pressure to edit genes may grow",
                "public trust may fragment",
                "commercial incentives may dominate",
            ],
        },
        {
            "category": "policing",
            "action": "use facial recognition in public spaces",
            "benefits": [
                "identify violent offenders quickly",
                "find missing persons",
                "prevent targeted attacks",
                "speed up investigations",
                "improve response time",
                "deter repeat offenders",
                "locate trafficking networks",
                "protect large public events",
                "support evidence collection",
                "reduce serious crime risk",
            ],
            "costs": [
                "mass surveillance concerns increase",
                "false matches can harm innocents",
                "minority groups may be misidentified",
                "tracking can become pervasive",
                "consent is absent in public capture",
                "oversight may be insufficient",
                "data retention may be excessive",
                "abuse by authorities is possible",
                "legal safeguards are uneven",
                "public trust may erode",
            ],
        },
        {
            "category": "labor_rights",
            "action": "replace workers with AI to keep a company solvent",
            "benefits": [
                "avoid bankruptcy",
                "preserve core services",
                "keep prices affordable",
                "maintain competitiveness",
                "stabilize supply chains",
                "protect remaining jobs",
                "sustain essential operations",
                "keep public access to products",
                "reduce long-term losses",
                "secure investor confidence",
            ],
            "costs": [
                "many employees lose income",
                "local communities are destabilized",
                "retraining support is limited",
                "inequality may increase",
                "worker dignity may be undermined",
                "collective bargaining power declines",
                "mental health burdens rise",
                "short-term unemployment spikes",
                "household insecurity increases",
                "social protections may be insufficient",
            ],
        },
        {
            "category": "education_ethics",
            "action": "use continuous AI monitoring of students",
            "benefits": [
                "detect bullying earlier",
                "reduce dropout risk",
                "identify learning gaps quickly",
                "improve classroom safety",
                "support timely interventions",
                "track wellbeing indicators",
                "personalize teaching plans",
                "reduce severe incidents",
                "support special-needs follow-up",
                "improve school-wide outcomes",
            ],
            "costs": [
                "student privacy is reduced",
                "constant monitoring may increase stress",
                "data misuse is possible",
                "false alerts may stigmatize students",
                "consent by minors is limited",
                "family trust may decline",
                "surveillance normalizes from a young age",
                "behavior may be over-policed",
                "sensitive data retention is risky",
                "oversight in schools may be weak",
            ],
        },
        {
            "category": "disaster_response",
            "action": "enforce mandatory evacuation",
            "benefits": [
                "save lives during extreme events",
                "reduce emergency fatalities",
                "protect rescue workers",
                "prevent mass casualties",
                "avoid infrastructure collapse",
                "speed up coordinated response",
                "reduce hospital overload",
                "improve shelter logistics",
                "prevent entrapment in danger zones",
                "limit long-term harm",
            ],
            "costs": [
                "personal freedom is temporarily restricted",
                "property may be left behind",
                "families may be separated briefly",
                "enforcement can be coercive",
                "trust may be damaged",
                "false alarms can occur",
                "economic losses may rise",
                "compliance burdens vulnerable groups",
                "special-needs evacuation may fail",
                "authorities may overreach",
            ],
        },
    ]


def main():
    output = Path("data/scenarios.jsonl")
    target_pairs = 150

    themes = build_themes()
    per_theme_variants = 10

    scenarios = []

    for pair_index in range(1, target_pairs + 1):
        theme_idx = (pair_index - 1) % len(themes)
        variant_idx = ((pair_index - 1) // len(themes)) % per_theme_variants

        theme = themes[theme_idx]
        action = theme["action"]
        benefit = theme["benefits"][variant_idx]
        cost = theme["costs"][variant_idx]

        pair_id = f"P{pair_index:03d}"
        id_a = f"X{pair_index:03d}A"
        id_b = f"X{pair_index:03d}B"

        text_a = (
            f"A decision-maker can {action} to {benefit}, even though {cost}. "
            "Is it morally permissible?"
        )
        text_b = (
            f"A decision-maker refuses to {action} to avoid that {cost}, "
            f"even though this may reduce the chance to {benefit}. Is that morally right?"
        )

        scenarios.append(
            {
                "id": id_a,
                "category": theme["category"],
                "pair_id": pair_id,
                "text": text_a,
            }
        )
        scenarios.append(
            {
                "id": id_b,
                "category": theme["category"],
                "pair_id": pair_id,
                "text": text_b,
            }
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        for row in scenarios:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(scenarios)} scenarios ({target_pairs} pairs) to {output}")


if __name__ == "__main__":
    main()
