from collections import defaultdict
from typing import List, Set, Tuple
from knowledge_base import Rule

class RuleInducer:
    def __init__(self, threshold=3):
        self.threshold = threshold
        # Dizionario: (frozenset(sintomi), guasto) -> conteggio
        self.candidate_counts = defaultdict(int)
    
    def add_observation(self, symptoms: Set[str], actual_fault: str, rules: List[Rule]):
        """
        Quando l'utente fornisce il guasto reale, controlla se esiste già una regola
        che copre esattamente quei sintomi con quella conclusione.
        Se no, incrementa il contatore per quella combinazione.
        """
        # Verifica se esiste già una regola con queste premesse e conclusione
        exists = any(
            set(r.premises) == symptoms and r.conclusion == actual_fault
            for r in rules
        )
        if not exists:
            key = (frozenset(symptoms), actual_fault)
            self.candidate_counts[key] += 1
    
    def get_candidates(self):
        """Restituisce le combinazioni che hanno superato la soglia."""
        candidates = []
        for (symptoms_frozen, fault), count in self.candidate_counts.items():
            if count >= self.threshold:
                candidates.append((set(symptoms_frozen), fault, count))
        return candidates
    
    def add_rule_from_candidate(self, symptoms: Set[str], fault: str, rules: List[Rule], probability=None):
        """Aggiunge una nuova regola alla lista rules."""
        if probability is None:
            # Probabilità iniziale come proporzione di occorrenze (ma non abbiamo il denominatore totale)
            # Per semplicità, usiamo 0.8 come default
            probability = 0.8
        new_rule = Rule(list(symptoms), fault, probability)
        rules.append(new_rule)
        # Rimuovi il candidato
        key = (frozenset(symptoms), fault)
        del self.candidate_counts[key]
