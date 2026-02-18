import csv
from dataclasses import dataclass
from typing import List, Set

@dataclass
class Rule:
    premises: List[str]   # lista di nomi di sintomi (classi)
    conclusion: str       # nome del guasto (classe)
    probability: float
    successes: int = 0
    total_uses: int = 0

def load_rules(filepath: str) -> List[Rule]:
    rules = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            premises = [p.strip() for p in row['premises'].split(',')]
            conclusion = row['conclusion'].strip()
            prob = float(row['probability'])
            rules.append(Rule(premises, conclusion, prob))
    return rules

def save_rules(filepath: str, rules: List[Rule]):
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['premises', 'conclusion', 'probability', 'successes', 'total_uses'])
        for r in rules:
            writer.writerow([','.join(r.premises), r.conclusion, r.probability])