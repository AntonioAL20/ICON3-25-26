import sys
import os
import csv
import random
import numpy as np

# Aggiunga della directory src al path per garantire che i moduli siano trovati
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge_base import load_rules, Rule
from inference import diagnose
from learning import update_probabilities
from induction import RuleInducer

def load_test_cases(filepath):
    cases = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symptoms = set(s.strip() for s in row['symptoms'].split(','))
            fault = row['true_fault'].strip()
            cases.append((symptoms, fault))
    return cases

def evaluate_fold(train_cases, test_cases, initial_rules, inducer_threshold=3):
    # Rule ha premesse come tupla, quindi è possibile creare nuove regole con le stesse premesse e conclusione
    rules = []
    for r in initial_rules:
        # Ricrea la regola con la stessa probabilità; le statistiche non vengono copiate
        rules.append(Rule(r.premises, r.conclusion, r.probability))
    
    inducer = RuleInducer(threshold=inducer_threshold)
    
    # Fase di training (apprendimento)
    for symptoms, true_fault in train_cases:
        results, used_rules = diagnose(symptoms, rules)
        #update_probabilities restituisce una nuova lista di regole
        rules = update_probabilities(rules, used_rules, true_fault, symptoms)
        inducer.add_observation(symptoms, true_fault, rules)
    
    #Aggiunta delle regole indotte alla fine del training
    for sym_set, fault, count in inducer.get_candidates():
        sym_tuple = tuple(sorted(sym_set))
        new_rule = Rule(sym_tuple, fault, 0.8)  # probabilità iniziale
        rules.append(new_rule)
    
    # Fase di test
    tp = 0  # veri positivi (guasto corretto predetto come primo)
    fp = 0
    fn = 0
    
    for symptoms, true_fault in test_cases:
        results, _ = diagnose(symptoms, rules)
        if not results:
            # Nessun guasto predetto
            if true_fault is not None:
                fn += 1
            continue
        # Prende il guasto con probabilità massima
        best_guess = max(results.items(), key=lambda x: x[1])[0]
        if best_guess == true_fault:
            tp += 1
        else:
            fp += 1
            fn += 1  # perché non è stato predetto il vero (assumendo che ci sia sempre un guasto vero)
    
    # Calcolo delle metriche
    accuracy = tp / len(test_cases) if test_cases else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    return accuracy, precision, recall

def cross_validation(cases, initial_rules, k=5, n_runs=10, inducer_threshold=3):
    accuracies = []
    precisions = []
    recalls = []
    
    for run in range(n_runs):
        random.shuffle(cases)
        fold_size = len(cases) // k
        run_acc = []
        run_prec = []
        run_rec = []
        for i in range(k):
            test = cases[i*fold_size:(i+1)*fold_size]
            train = cases[:i*fold_size] + cases[(i+1)*fold_size:]
            acc, prec, rec = evaluate_fold(train, test, initial_rules, inducer_threshold)
            run_acc.append(acc)
            run_prec.append(prec)
            run_rec.append(rec)
        accuracies.append(np.mean(run_acc))
        precisions.append(np.mean(run_prec))
        recalls.append(np.mean(run_rec))
    
    return {
        'accuracy_mean': np.mean(accuracies), 'accuracy_std': np.std(accuracies),
        'precision_mean': np.mean(precisions), 'precision_std': np.std(precisions),
        'recall_mean': np.mean(recalls), 'recall_std': np.std(recalls)
    }

if __name__ == '__main__':
    #percorso assoluto del file dei casi di test
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    test_cases_path = os.path.join(project_root, 'data', 'test_cases.csv')
    rules_path = os.path.join(project_root, 'data', 'rules_initial.csv')
    
    rules = load_rules(rules_path)
    cases = load_test_cases(test_cases_path)
    results = cross_validation(cases, rules, k=5, n_runs=10, inducer_threshold=2)
    
    print("Risultati cross-validation:")
    for key, value in results.items():
        print(f"{key}: {value:.4f}")
