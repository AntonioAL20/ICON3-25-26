import csv
import os
from dataclasses import dataclass
from typing import List, Tuple

def _get_project_root():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)

@dataclass(frozen=True)
class Rule:
    premises: Tuple[str, ...]  #lista di nomi di sintomi (classi)
    conclusion: str            #nome del guasto (classe)
    probability: float

def load_rules(relative_path: str) -> List[Rule]:
    full_path = os.path.join(_get_project_root(), relative_path)
    rules = []
    with open(full_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            premises = tuple(p.strip() for p in row['premises'].split(','))
            conclusion = row['conclusion'].strip()
            prob = float(row['probability'])
            rules.append(Rule(premises, conclusion, prob))
    return rules

def save_rules(relative_path: str, rules: List[Rule]):
    full_path = os.path.join(_get_project_root(), relative_path)
    with open(full_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['premises', 'conclusion', 'probability'])
        for r in rules:
            writer.writerow([','.join(r.premises), r.conclusion, r.probability])