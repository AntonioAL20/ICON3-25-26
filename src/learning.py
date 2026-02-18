from typing import List, Set
from knowledge_base import Rule

def update_probabilities(rules: List[Rule], used_rules: Set[Rule], correct_goal: str, observed: Set[str]):
    """
    Aggiorna le statistiche delle regole in base al feedback.
    Se correct_goal è None, significa che nessun guasto era presente (tutte le regole usate sono errate).
    """
    for rule in used_rules:
        rule.total_uses += 1
        if correct_goal is not None and rule.conclusion == correct_goal:
            rule.successes += 1
    # Ricalcola probabilità per tutte le regole
    for rule in rules:
        if rule.total_uses > 0:
            rule.probability = rule.successes / rule.total_uses
