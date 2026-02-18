from typing import List, Set, Dict, Tuple
from knowledge_base import Rule

def backward(goal: str, observed: Set[str], rules: List[Rule], used_rules: Set[Rule]) -> float:
    """
    Ritorna la probabilità massima tra le regole che dimostrano goal.
    goal è un nome di guasto (classe).
    observed è un insieme di nomi di sintomi osservati (classi).
    """
    if goal in observed:
        return 1.0   # i guasti non sono osservati direttamente, quindi questo caso non si verifica.
    max_prob = 0.0
    for rule in rules:
        if rule.conclusion == goal:
            # verifica tutte le premesse
            all_hold = True
            for p in rule.premises:
                if p not in observed:
                    all_hold = False
                    break
            if all_hold:
                if rule.probability > max_prob:
                    max_prob = rule.probability
                used_rules.add(rule)
    return max_prob

def diagnose(observed: Set[str], rules: List[Rule], ontology_mgr=None) -> Tuple[Dict[str, float], Set[Rule]]:
    """
    Restituisce un dizionario {guasto: probabilità} per tutti i guasti che hanno prob>0.
    observed: insieme di nomi di sintomi osservati.
    """
    # Estrai tutti i possibili guasti (conclusioni delle regole)
    all_conclusions = {r.conclusion for r in rules}
    results = {}
    used_rules_global = set()
    for goal in all_conclusions:
        used_local = set()
        prob = backward(goal, observed, rules, used_local)
        if prob > 0:
            results[goal] = prob
            used_rules_global.update(used_local)
    return results, used_rules_global
