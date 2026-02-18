from typing import List, Set, Dict, Tuple
from knowledge_base import Rule

# Dizionario per memorizzare le statistiche di ogni regola (successi, totale)
_stats: Dict[Rule, Tuple[int, int]] = {}

def update_probabilities(rules: List[Rule], used_rules: Set[Rule], correct_goal: str, observed: Set[str]) -> List[Rule]:
    """
    Aggiorna le statistiche per le regole usate e restituisce una nuova lista di regole
    con le probabilità ricalcolate.
    """
    global _stats
    
    # Aggiorna le statistiche per ogni regola usata
    for rule in used_rules:
        successes, total = _stats.get(rule, (0, 0))
        total += 1
        if correct_goal is not None and rule.conclusion == correct_goal:
            successes += 1
        _stats[rule] = (successes, total)
    
    # Ricrea la lista delle regole con le probabilità aggiornate
    new_rules = []
    for rule in rules:
        successes, total = _stats.get(rule, (0, 0))
        if total > 0:
            new_prob = successes / total
        else:
            new_prob = rule.probability  # probabilità iniziale se mai usata
        new_rule = Rule(rule.premises, rule.conclusion, new_prob)
        new_rules.append(new_rule)
    
    return new_rules