from collections import defaultdict
from typing import List, Set, Tuple
from knowledge_base import Rule

class RuleInducer:
    def __init__(self, threshold=3):
        self.threshold = threshold  # Soglia per proporre una nuova regola
        self.candidate_counts = defaultdict(int)  # Contatore per coppie (sintomi, guasto) non ancora regole

    def add_observation(self, symptoms: Set[str], actual_fault: str, rules: List[Rule]):
        # Crea una tupla ordinata per usare l'insieme come chiave hashable
        sym_tuple = tuple(sorted(symptoms))
        # Verifica se esiste già una regola con queste premesse e conclusione
        exists = any(
            r.premises == sym_tuple and r.conclusion == actual_fault
            for r in rules
        )
        if not exists:
            key = (sym_tuple, actual_fault)
            self.candidate_counts[key] += 1  # Incrementa il contatore del candidato

    def get_candidates(self):
        candidates = []
        for (sym_tuple, fault), count in self.candidate_counts.items():
            if count >= self.threshold:
                # Restituisce i sintomi come set per comodità
                candidates.append((set(sym_tuple), fault, count))
        return candidates

    def add_rule_from_candidate(self, symptoms: Set[str], fault: str, rules: List[Rule], probability=None):
        sym_tuple = tuple(sorted(symptoms))
        if probability is None:
            probability = 0.8  # Probabilità di default per le nuove regole
        new_rule = Rule(sym_tuple, fault, probability)
        rules.append(new_rule)  # Aggiunge la nuova regola alla KB
        key = (sym_tuple, fault)
        if key in self.candidate_counts:
            del self.candidate_counts[key]  # Rimuove il candidato dopo l'uso
