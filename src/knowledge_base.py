import csv
import os
from dataclasses import dataclass
from typing import List, Tuple

def _get_project_root():
    """Restituisce il percorso assoluto della directory principale del progetto."""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # cartella src/
    return os.path.dirname(current_dir)                        # risale alla root

@dataclass(frozen=True)
class Rule:
    """Classe immutabile che rappresenta una regola: premesse, conclusione e probabilità."""
    premises: Tuple[str, ...]  # lista ordinata di nomi di sintomi (classi)
    conclusion: str            # nome del guasto (classe)
    probability: float         # probabilità associata alla regola

def load_rules(relative_path: str) -> List[Rule]:
    """Carica le regole da un file CSV e restituisce una lista di oggetti Rule."""
    full_path = os.path.join(_get_project_root(), relative_path)  # percorso assoluto
    rules = []
    with open(full_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Converte la stringa delle premesse in una tupla ordinata
            premises = tuple(p.strip() for p in row['premises'].split(','))
            conclusion = row['conclusion'].strip()
            prob = float(row['probability'])
            rules.append(Rule(premises, conclusion, prob))
    return rules

def save_rules(relative_path: str, rules: List[Rule]):
    """Salva la lista di regole in un file CSV sovrascrivendo il contenuto."""
    full_path = os.path.join(_get_project_root(), relative_path)
    with open(full_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['premises', 'conclusion', 'probability'])  # intestazione
        for r in rules:
            # Ricostruisce la stringa delle premesse unendo la tupla con virgole
            writer.writerow([','.join(r.premises), r.conclusion, r.probability])
