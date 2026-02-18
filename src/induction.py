from collections import defaultdict
from typing import List, Set, Tuple
from knowledge_base import Rule

class RuleInducer:
    def __init__(self, threshold=3):
        self.threshold = threshold
        self.candidate_counts = defaultdict(int)
    
    def add_observation(self, symptoms: Set[str], actual_fault: str, rules: List[Rule]):
        sym_tuple = tuple(sorted(symptoms))
        exists = any(
            r.premises == sym_tuple and r.conclusion == actual_fault
            for r in rules
        )
        if not exists:
            key = (sym_tuple, actual_fault)
            self.candidate_counts[key] += 1
    
    def get_candidates(self):
        candidates = []
        for (sym_tuple, fault), count in self.candidate_counts.items():
            if count >= self.threshold:
                candidates.append((set(sym_tuple), fault, count))
        return candidates
    
    def add_rule_from_candidate(self, symptoms: Set[str], fault: str, rules: List[Rule], probability=None):
        sym_tuple = tuple(sorted(symptoms))
        if probability is None:
            probability = 0.8
        new_rule = Rule(sym_tuple, fault, probability)
        rules.append(new_rule)
        key = (sym_tuple, fault)
        if key in self.candidate_counts:
            del self.candidate_counts[key]